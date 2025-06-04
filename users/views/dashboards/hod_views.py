# users/views/dashboards/hod_views.py
"""
Views for Head of Department (HOD) dashboards and related student data.
Includes role-restricted access and structured subject/student insights.
"""

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404

# Models
from users.models import Student
from the_school.models import Subject
from exams.models import StudentMark

# Context & Services
from users.services.teacher_based_context.v2_subject_performance_context import get_subject_performance_context
from users.services.teacher_based_services.v2_student_card_service import get_student_card_context_for_teacher
from users.services.context.v2_student_dashboard_context import get_full_student_context
from users.services.context.v2_student_metadata_context import build_student_subject_metadata_context
from users.services.context.v2_student_exam_insights_context import get_exam_results_context
from users.services.context.v2_student_exam_highlights import get_student_exam_highlights
from users.services.context.v2_student_grade_insights_context import build_grade_insights_context
from users.services.context.v2_exam_report_final_context import build_exam_report_context
from users.services.context.v2_student_exam_performance_context import build_student_exam_performance_context
from users.services.context.v2_1_student_subject_comments_context import build_student_subject_comments_context
from users.services.context.v2_student_teacher_contact_context import build_student_teacher_contact_context
from users.services.student_dashboard_service import get_student_exam_schedule
from users.services.teacher_based_services.student_performance_chart_service import get_chart_data_list_for_teacher

# Role verification

def is_hod(user):
    return user.is_authenticated and hasattr(user, "teacher") and user.teacher.teacher_role == "HOD"

# -------------------------
# HOD DASHBOARD
# -------------------------

@login_required
@user_passes_test(is_hod)
def hod_dashboard(request):
    return render(request, 'dashboards/hod_teacher/hod_teacher_dashboard.html')


# -------------------------
# Subject Performance Summary
# -------------------------

@login_required
@user_passes_test(is_hod)
def hod_view_subject_performance(request):
    teacher = request.user.teacher
    context = get_subject_performance_context(teacher)
    return render(request, "dashboards/hod_teacher/hod_view_subject_performance.html", context)


# -------------------------
# List of Department Students
# -------------------------

@login_required
@user_passes_test(is_hod)
def hod_view_student_view(request):
    context = get_student_card_context_for_teacher(request)
    return render(request, "dashboards/hod_teacher/hod_view_student.html", context)


# -------------------------
# Full Student Hub View
# -------------------------

@login_required
@user_passes_test(is_hod)
def hod_view_studenthub_dashboard(request, student_id):
    teacher = request.user.teacher
    student = get_object_or_404(Student, id=student_id)

    subject_ids = Subject.objects.filter(
        department__head_of_department=teacher
    ).values_list("id", flat=True)

    has_marks = StudentMark.objects.filter(
        student=student, exam__subject_id__in=subject_ids
    ).exists()

    if not has_marks:
        return render(request, "errors/403.html", status=403)

    context = get_full_student_context(student)
    return render(request, "dashboards/hod_teacher/hod_view_studenthub_dashboard.html", context)


# -------------------------
# Role Validation for Access
# -------------------------

def verify_hod_access(user, student):
    teacher = getattr(user, "teacher", None)
    if not teacher:
        return False
    subject_ids = Subject.objects.filter(
        department__head_of_department=teacher
    ).values_list("id", flat=True)
    return StudentMark.objects.filter(
        student=student, exam__subject_id__in=subject_ids
    ).exists()


# -------------------------
# Student Subviews
# -------------------------

@login_required
@user_passes_test(is_hod)
def hod_student_subjects_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not verify_hod_access(request.user, student):
        return render(request, "errors/403.html", status=403)
    context = build_student_subject_metadata_context(student)
    return render(request, "dashboards/hod_teacher/hod_view_subjects.html", context)


@login_required
@user_passes_test(is_hod)
def hod_exam_results_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not verify_hod_access(request.user, student):
        return render(request, "errors/403.html", status=403)
    context = get_exam_results_context(student)
    context.update(get_student_exam_highlights(student))
    context["student"] = student
    return render(request, "dashboards/hod_teacher/hod_view_exam_results.html", context)


@login_required
@user_passes_test(is_hod)
def hod_exam_timetable_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not verify_hod_access(request.user, student):
        return render(request, "errors/403.html", status=403)
    schedule = get_student_exam_schedule(student)
    context = {"student": student, "exams": schedule.get("exams", [])}
    return render(request, "dashboards/hod_teacher/hod_view_exam_timetable.html", context)


@login_required
@user_passes_test(is_hod)
def hod_grade_insights_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not verify_hod_access(request.user, student):
        return render(request, "errors/403.html", status=403)
    context = build_grade_insights_context(student)
    return render(request, "dashboards/hod_teacher/hod_view_grade_insights.html", context)


@login_required
@user_passes_test(is_hod)
def hod_report_card_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not verify_hod_access(request.user, student):
        return render(request, "errors/403.html", status=403)
    context = build_exam_report_context(student)
    return render(request, "dashboards/hod_teacher/hod_view_report_card.html", context)


@login_required
@user_passes_test(is_hod)
def hod_printable_report_card(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not verify_hod_access(request.user, student):
        return render(request, "errors/403.html", status=403)
    context = build_exam_report_context(student)
    return render(request, "pdf/_pdf_student_report.html", context)


@login_required
@user_passes_test(is_hod)
def hod_performance_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not verify_hod_access(request.user, student):
        return render(request, "errors/403.html", status=403)
    context = build_student_exam_performance_context(student)
    return render(request, "dashboards/hod_teacher/hod_view_performance.html", context)


@login_required
@user_passes_test(is_hod)
def hod_subject_comments_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not verify_hod_access(request.user, student):
        return render(request, "errors/403.html", status=403)
    context = build_student_subject_comments_context(student)
    return render(request, "dashboards/hod_teacher/hod_view_comments.html", context)


@login_required
@user_passes_test(is_hod)
def hod_contact_teachers_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not verify_hod_access(request.user, student):
        return render(request, "errors/403.html", status=403)
    context = build_student_teacher_contact_context(student)
    return render(request, "dashboards/hod_teacher/hod_view_contacts.html", context)


# -------------------------
# Subject Performance Charts (HOD)
# -------------------------

@login_required
@user_passes_test(is_hod)
def hod_student_charts_view(request):
    chart_data_list = get_chart_data_list_for_teacher(request)
    return render(request, "dashboards/hod_teacher/hod_view_charts.html", {
        "chart_data_list": chart_data_list
    })
