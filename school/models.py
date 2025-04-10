from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

class Address(models.Model):
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default="Not stated")
    
    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.state} {self.postal_code}"

class AcademicYear(models.Model):
    name = models.CharField(max_length=50)  # e.g., "2023-2024"
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return self.name

# Removed Semester class

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    date_joined = models.DateField(auto_now_add=True)
    
    class Role(models.TextChoices):
        STUDENT = 'STUDENT', 'Student'
        TEACHER = 'TEACHER', 'Teacher'
        PARENT = 'PARENT', 'Parent'
        STAFF = 'STAFF', 'Staff'
    
    role = models.CharField(max_length=10, choices=Role.choices)
    
    class Meta:
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"

class Student(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True,
                                limit_choices_to={'role': Person.Role.STUDENT})
    admission_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.person} - {self.pk}"

class Parent(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True,
                                limit_choices_to={'role': Person.Role.PARENT})
    occupation = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.person}"

class Teacher(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True,
                                limit_choices_to={'role': Person.Role.TEACHER})
    qualification = models.CharField(max_length=100, blank=True)
    joining_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.person} ({self.pk})"

class Staff(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True,
                                limit_choices_to={'role': Person.Role.STAFF})
    department = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.person} - {self.position}"

class Class(models.Model):
    name = models.CharField(max_length=50)  # e.g., "Class 10A"
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Subject(models.Model):
    SUBJECT_CHOICES = [
        ('English', 'English'),
        ('Math', 'Math'),
        ('Art', 'Art'),
        ('Science', 'Science'),
        ('History', 'History'),
        ('Music', 'Music'),
        ('Geography', 'Geography'),
        ('P.E', 'P.E (Physical Education)'),
        ('Drama', 'Drama'),
        ('Biology', 'Biology'),
        ('Chemistry', 'Chemistry'),
        ('Physics', 'Physics'),
        ('I.T', 'I.T (Information Technology)'),
        ('Foreign Languages', 'Foreign Languages'),
        ('Social Studies', 'Social Studies'),
        ('Technology', 'Technology'),
        ('Philosophy', 'Philosophy'),
        ('Graphic Design', 'Graphic Design'),
        ('Literature', 'Literature'),
        ('Algebra', 'Algebra'),
        ('Geometry', 'Geometry'),
    ]
    
    name = models.CharField(max_length=100, choices=SUBJECT_CHOICES, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"

class ClassEnrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    date_enrolled = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'class_obj', 'academic_year')
        ordering = ['academic_year', 'class_obj']
    
    def __str__(self):
        return f"{self.student} in {self.class_obj} ({self.academic_year})"

class ParentChildRelationship(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    child = models.ForeignKey(Student, on_delete=models.CASCADE)
    relationship = models.CharField(max_length=50)  # e.g., "Mother", "Father", "Guardian"
    
    class Meta:
        unique_together = ('parent', 'child')
    
    def __str__(self):
        return f"{self.parent} is {self.relationship} of {self.child}"

class Exam(models.Model):
    EXAM_TYPES = [
        ('MID', 'Mid-Term'),
        ('FINAL', 'Final'),
        ('QUIZ', 'Quiz'),
        ('PROJECT', 'Project'),
    ]
    
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)  # Updated subject field
    exam_type = models.CharField(max_length=10, choices=EXAM_TYPES)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    total_marks = models.PositiveIntegerField(default=100)
    date_conducted = models.DateField()
    
    class Meta:
        ordering = ['academic_year', 'date_conducted']
    
    def __str__(self):
        return f"{self.subject} ({self.exam_type} - {self.academic_year})"  # Updated __str__

class Grade(models.Model):
    GRADE_CHOICES = [
        ('A', 'A (Excellent)'),
        ('B', 'B (Very Good)'),
        ('C', 'C (Good)'),
        ('D', 'D (Satisfactory)'),
        ('E', 'E (Pass)'),
        ('F', 'F (Fail)'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    marks_obtained = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES)
    remarks = models.TextField(blank=True)
    graded_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    date_graded = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'subject', 'exam')
        ordering = ['exam__academic_year', 'subject']
    
    def save(self, *args, **kwargs):
        # Auto-calculate grade based on marks
        if self.marks_obtained >= 90:
            self.grade = 'A'
        elif self.marks_obtained >= 80:
            self.grade = 'B'
        elif self.marks_obtained >= 70:
            self.grade = 'C'
        elif self.marks_obtained >= 60:
            self.grade = 'D'
        elif self.marks_obtained >= 50:
            self.grade = 'E'
        else:
            self.grade = 'F'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.student} - {self.subject}: {self.grade} ({self.exam})"

class ClassSubjectTeacher(models.Model):
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('class_obj', 'subject', 'academic_year')
        ordering = ['academic_year', 'class_obj']
    
    def __str__(self):
        return f"{self.class_obj} - {self.subject} by {self.teacher} ({self.academic_year})"

# Signal to automatically create corresponding inactive entries
@receiver(post_save, sender=Person)
def create_role_instance(sender, instance, created, **kwargs):
    if created:
        if instance.role == Person.Role.STUDENT:
            Student.objects.create(person=instance, is_active=False)
        elif instance.role == Person.Role.TEACHER:
            Teacher.objects.create(person=instance, is_active=False)
        elif instance.role == Person.Role.PARENT:
            Parent.objects.create(person=instance, is_active=False)
        elif instance.role == Person.Role.STAFF:
            Staff.objects.create(person=instance, is_active=False)