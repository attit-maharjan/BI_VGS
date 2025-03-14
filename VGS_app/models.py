from django.db import models
from django.contrib.auth.models import User


# Roles Table
class Role(models.Model):
    role_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.role_name

# People Table (common table for everyone)
class Person(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

# Student Details
class StudentDetails(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True)
    enrollment_number = models.CharField(max_length=50, unique=True)
    guardian_name = models.CharField(max_length=100)

# Teacher Details
class TeacherDetails(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True)
    qualification = models.CharField(max_length=100)
    hire_date = models.DateField()

# Parent-Student Relation (Ensuring only Parents can be linked)
class ParentStudent(models.Model):
    parent = models.ForeignKey(
        Person, 
        on_delete=models.CASCADE, 
        related_name='children',
        limit_choices_to={'role__role_name': 'Parent'}  
    )
    student = models.ForeignKey(
        Person, 
        on_delete=models.CASCADE, 
        related_name='parents',
        limit_choices_to={'role__role_name': 'Student'}  
    )

    class Meta:
        unique_together = ('parent', 'student')

# Academic Year
class AcademicYear(models.Model):
    year = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

# Class
class Class(models.Model):
    class_name = models.CharField(max_length=50, unique=True)

# Subject (Now includes is_active field)
class Subject(models.Model):
    subject_name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)  

# ClassSubject (which subjects each class has)
class ClassSubject(models.Model):
    class_model = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='subjects')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('class_model', 'subject')

# Student Enrollment
class StudentEnrollment(models.Model):
    student = models.ForeignKey(Person, on_delete=models.CASCADE, limit_choices_to={'role__role_name': 'Student'})
    class_model = models.ForeignKey(Class, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)

# Grades
class Grade(models.Model):
    student = models.ForeignKey(Person, on_delete=models.CASCADE, limit_choices_to={'role__role_name': 'Student'})
    class_subject = models.ForeignKey(ClassSubject, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    marks_obtained = models.FloatField()

# ReportCard (Tracking student progression over the years)
class ReportCardSnapshot(models.Model):
    student = models.ForeignKey(Person, on_delete=models.CASCADE, limit_choices_to={'role__role_name': 'Student'})
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    overall_percentage = models.FloatField()
    overall_grade = models.CharField(max_length=5)
    remarks = models.TextField()
    issue_date = models.DateField(auto_now_add=True)

    # Link to previous year's report
    previous_year_report = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )

class AcademicEvent(models.Model):
    date = models.DateField()  # Date of the event
    title = models.CharField(max_length=255)  # Title of the event (e.g., Lecture, Exam)
    description = models.TextField()  # Detailed description of the event
    event_type = models.CharField(max_length=50)  # Event type (e.g., "Exam", "Lecture", "Holiday")
    
    def __str__(self):
        return f'{self.title} on {self.date}'