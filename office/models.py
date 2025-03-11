from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Person(models.Model):
    ROLE_CHOICES = [
        ("STUDENT", "Student"),
        ("TEACHER", "Teacher"),
        ("PARENT", "Parent")
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True, db_index=True)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class StudentDetails(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True)
    enrollment_number = models.CharField(max_length=50, unique=True)
    guardian_name = models.CharField(max_length=100)

class TeacherDetails(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True)
    qualification = models.CharField(max_length=100)
    hire_date = models.DateField()

class ParentStudentAssociation(models.Model):
    parent = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='children', limit_choices_to={'role': 'PARENT'})
    student = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='parents', limit_choices_to={'role': 'STUDENT'})

    class Meta:
        unique_together = ('parent', 'student')

    def clean(self):
        if self.parent.role != "PARENT":
            raise ValidationError("Parent must have a parent role.")
        if self.student.role != "STUDENT":
            raise ValidationError("Student must have a student role.")

class AcademicYear(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()

    @property
    def year(self):
        return self.start_date.year

class Class(models.Model):
    class_name = models.CharField(max_length=50, unique=True)

class Subject(models.Model):
    class Genre(models.TextChoices):
        COMPULSORY = 'COMP', _('Compulsory')
        ELECTIVE = 'ELEC', _('Elective')

    class CompulsorySubjects(models.TextChoices):
        MATHEMATICS = 'MATH', _('Mathematics')
        SCIENCE = 'SCI', _('Science')
        ENGLISH = 'ENG', _('English')
        HISTORY = 'HIST', _('History')
        # Add more compulsory subjects as needed

    class ElectiveSubjects(models.TextChoices):
        ART = 'ART', _('Art')
        MUSIC = 'MUS', _('Music')
        COMPUTER_SCIENCE = 'CS', _('Computer Science')
        FOREIGN_LANGUAGE = 'LANG', _('Foreign Language')
        # Add more elective subjects as needed

    subject_name = models.CharField(max_length=50, unique=True)
    genre = models.CharField(
        max_length=4,
        choices=Genre.choices,
        default=Genre.COMPULSORY
    )
    subject_code = models.CharField(
        max_length=4,
        choices=CompulsorySubjects.choices + ElectiveSubjects.choices,
        unique=True,
        default='DEFAULT'
    )

    def __str__(self):
        return f"{self.get_subject_code_display()} ({self.get_genre_display()})"

    def save(self, *args, **kwargs):
        if self.subject_code in dict(self.CompulsorySubjects.choices):
            self.genre = self.Genre.COMPULSORY
        elif self.subject_code in dict(self.ElectiveSubjects.choices):
            self.genre = self.Genre.ELECTIVE
        super().save(*args, **kwargs)

class ClassSubject(models.Model):
    class_model = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='subjects')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ('class_model', 'subject', 'academic_year')


class StudentEnrollment(models.Model):
    student = models.ForeignKey(Person, on_delete=models.CASCADE, limit_choices_to={'role': 'STUDENT'})
    class_model = models.ForeignKey(Class, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True, db_index=True)
    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("COMPLETED", "Completed"),
        ("WITHDRAWN", "Withdrawn")
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="ACTIVE")

    class Meta:
        unique_together = ('student', 'class_model', 'academic_year')

class Grade(models.Model):
    student = models.ForeignKey(Person, on_delete=models.CASCADE, limit_choices_to={'role': 'STUDENT'})
    class_subject = models.ForeignKey(ClassSubject, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    marks_obtained = models.FloatField()
    max_marks = models.FloatField(default=100.0)

    @property
    def percentage(self):
        return (self.marks_obtained / self.max_marks) * 100

class ReportCardSnapshot(models.Model):
    student = models.ForeignKey(Person, on_delete=models.CASCADE, limit_choices_to={'role': 'STUDENT'})
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    overall_percentage = models.FloatField()
    overall_grade = models.CharField(max_length=5)
    remarks = models.TextField()
    issue_date = models.DateField(auto_now_add=True)
    finalized = models.BooleanField(default=False)
