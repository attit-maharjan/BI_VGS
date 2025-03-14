from django.contrib import admin
from .models import (
    Person, StudentDetails, TeacherDetails, ParentStudentAssociation,
    AcademicYear, Class, Subject, ClassSubject,
    StudentEnrollment, Grade, ReportCardSnapshot
)

class ParentStudentAssociationInline(admin.TabularInline):
    model = ParentStudentAssociation
    fk_name = 'student'
    extra = 1
    autocomplete_fields = ['parent']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            kwargs["queryset"] = Person.objects.filter(role='PARENT')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class StudentDetailsInline(admin.StackedInline):
    model = StudentDetails
    extra = 1

class TeacherDetailsInline(admin.StackedInline):
    model = TeacherDetails
    extra = 1

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'role', 'email', 'date_of_birth')
    list_filter = ('role',)
    search_fields = ('first_name', 'last_name', 'email')
    inlines = [StudentDetailsInline, TeacherDetailsInline, ParentStudentAssociationInline]
    
    def get_inline_instances(self, request, obj=None):
        if obj and obj.role == 'STUDENT':
            return [inline(self.model, self.admin_site) for inline in inlines]
        return []

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Name'

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('year', 'start_date', 'end_date')
    ordering = ('-start_date',)

@admin.register(ClassSubject)
class ClassSubjectAdmin(admin.ModelAdmin):
    list_display = ('class_model', 'subject', 'academic_year')
    list_filter = ('academic_year', 'class_model')
    autocomplete_fields = ['class_model', 'subject']
    search_fields = ['class_model__class_name', 'subject__subject_name']

@admin.register(StudentEnrollment)
class StudentEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_model', 'academic_year', 'status')
    list_filter = ('academic_year', 'class_model', 'status')
    search_fields = ('student__first_name', 'student__last_name')
    autocomplete_fields = ['student', 'class_model']

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_subject', 'marks_obtained', 'percentage')
    list_filter = ('academic_year', 'class_subject__class_model')
    search_fields = ('student__first_name', 'student__last_name')

    def percentage(self, obj):
        return f"{obj.percentage:.1f}%"
    percentage.admin_order_field = 'marks_obtained'

@admin.register(ReportCardSnapshot)
class ReportCardSnapshotAdmin(admin.ModelAdmin):
    list_display = ('student', 'academic_year', 'overall_percentage', 'finalized')
    list_filter = ('academic_year', 'finalized')
    search_fields = ('student__first_name', 'student__last_name')

# Basic registrations for simple models
@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    search_fields = ['class_name']
    list_display = ('class_name',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_name', 'get_subject_code_display', 'get_genre_display')
    list_filter = ('genre',)
    search_fields = ('subject_name', 'subject_code')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['subject_code'].widget.choices = (
            Subject.CompulsorySubjects.choices + Subject.ElectiveSubjects.choices
        )
        return form
