from django.contrib import admin
from .models import (
    Role, Person, StudentDetails, TeacherDetails, ParentStudent,
    AcademicYear, Class, Subject, ClassSubject,
    StudentEnrollment, Grade, ReportCardSnapshot
)

admin.site.register(Role)
admin.site.register(Person)
admin.site.register(StudentDetails)
admin.site.register(TeacherDetails)
admin.site.register(ParentStudent)
admin.site.register(AcademicYear)
admin.site.register(Class)
admin.site.register(Subject)
admin.site.register(ClassSubject)
admin.site.register(StudentEnrollment)
admin.site.register(Grade)
admin.site.register(ReportCardSnapshot)