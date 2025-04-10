from django.contrib import admin
from .models import *

class AddressAdmin(admin.ModelAdmin):
    list_display = ('street_address', 'city', 'state', 'postal_code', 'country')
    search_fields = ('street_address', 'city', 'state', 'postal_code')
    list_filter = ('city', 'state', 'country')

class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_current')
    list_editable = ('is_current',)
    ordering = ('-start_date',)
    actions = ['set_as_current']
    search_fields = ('name',)

    def set_as_current(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "Please select exactly one academic year to set as current.", level='ERROR')
            return
        AcademicYear.objects.update(is_current=False)
        queryset.update(is_current=True)
        self.message_user(request, "Selected academic year is now set as current.")
    set_as_current.short_description = "Set selected year as current"

# Removed SemesterAdmin class

class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'role', 'date_joined')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    list_filter = ('role', 'date_joined')
    ordering = ('last_name', 'first_name')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('person', 'admission_date', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('person__first_name', 'person__last_name', 'person__email')

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('person', 'occupation', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('person__first_name', 'person__last_name', 'person__email')

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('person', 'qualification', 'joining_date', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('person__first_name', 'person__last_name', 'person__email')

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('person', 'department', 'position', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('person__first_name', 'person__last_name', 'person__email')

class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'description_short')
    search_fields = ('name', 'code')
    
    def description_short(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_short.short_description = 'Description'

class ClassEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_obj', 'academic_year')
    list_filter = ('class_obj', 'academic_year')
    search_fields = ('student__person__first_name', 'student__person__last_name')
    autocomplete_fields = ('student', 'class_obj', 'academic_year')

class ParentChildRelationshipAdmin(admin.ModelAdmin):
    list_display = ('parent', 'child', 'relationship')
    list_filter = ('relationship',)
    search_fields = ('parent__person__first_name', 'parent__person__last_name', 
                    'child__person__first_name', 'child__person__last_name')
    autocomplete_fields = ('parent', 'child')

class ExamAdmin(admin.ModelAdmin):
    list_display = ('subject', 'exam_type', 'academic_year', 'date_conducted')
    list_filter = ('exam_type', 'academic_year')
    date_hierarchy = 'date_conducted'
    ordering = ('-date_conducted',)
    autocomplete_fields = ('subject', 'academic_year')
    search_fields = ('subject__name', 'exam_type', 'academic_year__name')  # Added search_fields

class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'exam', 'marks_obtained', 'grade', 'graded_by')
    list_filter = ('grade', 'subject', 'exam__academic_year')
    autocomplete_fields = ('student', 'subject', 'exam', 'graded_by')
    list_editable = ('marks_obtained', 'grade')

class ClassSubjectTeacherAdmin(admin.ModelAdmin):
    list_display = ('class_obj', 'subject', 'teacher', 'academic_year')  # Removed 'semester'
    list_filter = ('academic_year', 'teacher')  # Removed 'semester'
    search_fields = ('class_obj__name', 'subject__name', 'teacher__person__first_name', 'teacher__person__last_name')
    autocomplete_fields = ('class_obj', 'subject', 'teacher', 'academic_year')  # Removed 'semester'

# Register all models
admin.site.register(Address, AddressAdmin)
admin.site.register(AcademicYear, AcademicYearAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(ClassEnrollment, ClassEnrollmentAdmin)
admin.site.register(ParentChildRelationship, ParentChildRelationshipAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(ClassSubjectTeacher, ClassSubjectTeacherAdmin)