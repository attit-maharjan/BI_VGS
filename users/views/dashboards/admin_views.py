# users/views/dashboards/admin_views.py

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from users.forms_crud_transactions.admin_register_user import AdminRegisterUserForm
from users.forms_crud_transactions.school_settings_form import SchoolSettingsForm
from users.models import Student, User
from enrollments.models import ClassGroupStudentEnrollment
from the_school.models import SchoolSettings


# ------------------------------------------------------------------------------
# Utility: Restrict access to admins only
# ------------------------------------------------------------------------------
def is_admin(user):
    return user.is_authenticated and user.role == 'admin'


# ------------------------------------------------------------------------------
# View: Admin Dashboard
# Renders the admin home page with overview actions
# ------------------------------------------------------------------------------
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'dashboards/admin/admin_dashboard.html')


# ------------------------------------------------------------------------------
# View: Register New User
# Allows admin to register a student or admin account
# ------------------------------------------------------------------------------
@login_required
@user_passes_test(is_admin)
def admin_register_user_view(request):
    form = AdminRegisterUserForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                f"User '{user.get_full_name()}' ({user.role.upper()}) registered successfully."
            )
            return redirect("users:admin_dashboard")
        else:
            messages.error(request, "Please correct the errors below.")

    return render(request, "dashboards/admin/admin_register_user.html", {"form": form})


# ------------------------------------------------------------------------------
# View: Unassigned Students
# Lists students not yet enrolled in any class group
# ------------------------------------------------------------------------------
@login_required
@user_passes_test(is_admin)
def unassigned_students_view(request):
    assigned_student_ids = ClassGroupStudentEnrollment.objects.values_list('student_id', flat=True)
    unassigned_students = Student.objects.exclude(id__in=assigned_student_ids).select_related('user')

    return render(request, "dashboards/admin/unassigned_students.html", {
        "students": unassigned_students
    })


# ------------------------------------------------------------------------------
# View: Delete Unassigned Student
# Removes student and linked user account if unassigned
# ------------------------------------------------------------------------------
@login_required
@user_passes_test(is_admin)
def delete_unassigned_student_view(request, student_id):
    if request.method == "POST":
        try:
            student = Student.objects.get(student_id=student_id)
            full_name = student.user.get_full_name()
            student.user.delete()
            messages.success(request, f"Student '{full_name}' deleted successfully.")
        except Student.DoesNotExist:
            messages.error(request, "Student not found or already deleted.")
        return redirect("users:admin_unassigned_students")

    return HttpResponseRedirect(reverse("users:admin_unassigned_students"))


# ------------------------------------------------------------------------------
# View: Update School Settings
# Displays and updates the school’s configuration (singleton form)
# ------------------------------------------------------------------------------
@login_required
@user_passes_test(is_admin)
def admin_update_school_settings_view(request):
    instance = SchoolSettings.objects.first()
    form = SchoolSettingsForm(request.POST or None, request.FILES or None, instance=instance)

    if request.method == "POST":
        if form.has_changed():
            if form.is_valid():
                form.save()
                messages.success(request, "School settings updated successfully.")
                return redirect("users:admin_update_school_settings")
            else:
                messages.error(request, "Please correct the errors below.")
        else:
            messages.info(request, "No changes detected. Settings were not updated.")

    return render(request, "dashboards/admin/update_school_settings.html", {"form": form})
