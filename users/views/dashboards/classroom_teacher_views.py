# users/views/dashboards/classroom_teacher_views.py
"""
View definitions for classroom teachers' dashboards and student interactions.
Follows clear structure with grouped imports and reusable context services.
"""

# ==========================
# Imports
# ==========================

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect

# Models
from users.models import Student, Teacher, User
from enrollments.models import ClassGroupStudentEnrollment
from the_school.models import SchoolSettings

# Context Services - Student Dashboard
from users.services.context.v2_student_dashboard_context import get_full_student_context
from users.services.context.v2_student_metadata_context import build_student_subject_metadata_context
from users.services.context.v2_student_exam_insights_context import get_exam_results_context
from users.services.context.v2_student_grade_insights_context import build_grade_insights_context
from users.services.context.v2_exam_report_final_context import build_exam_report_context
from users.services.context.v2_student_exam_performance_context import build_student_exam_performance_context
from users.services.context.v2_1_student_subject_comments_context import build_student_subject_comments_context
from users.services.context.v2_student_teacher_contact_context import build_student_teacher_contact_context
from users.services.student_dashboard_service import get_student_exam_schedule
from users.services.context.v2_student_exam_highlights import get_student_exam_highlights

# Context Services - Teacher Based
from users.services.teacher_based_context.v2_subject_performance_context import get_subject_performance_context
from users.services.teacher_based_services.v2_student_card_service import (
    get_students_for_teacher,
    get_student_card_context_for_teacher,
)
from users.services.teacher_based_services.student_performance_chart_service import get_chart_data_list_for_teacher


# ==========================
# Dashboard Views
# ==========================

@login_required
def classroom_teacher_dashboard(request):
    context = {"name": "Philip"}  # TODO: Replace with real data context if needed
    return render(request, "dashboards/classroom_teacher/classroom_teacher_dashboard.html", context)


# ==========================
# Student Hub & Subviews
# ==========================

def verify_classroom_teacher_access(user, student):
    teacher = getattr(user, "teacher", None)
    return teacher and ClassGroupStudentEnrollment.objects.filter(
        student=student,
        class_group__in=teacher.classgroup_assignments.values_list("class_group", flat=True),
        is_active=True
    ).exists()


@login_required
def classroom_teacher_view_studenthub_dashboard(request, student_id):
    teacher = request.user.teacher
    classgroup_assignment = teacher.classgroup_assignments.filter(is_active=True).first()
    if not classgroup_assignment:
        return render(request, "errors/403.html", status=403)

    enrollment = get_object_or_404(
        ClassGroupStudentEnrollment,
        student_id=student_id,
        class_group=classgroup_assignment.class_group,
        is_active=True
    )
    context = get_full_student_context(enrollment.student)
    return render(request, "dashboards/classroom_teacher/classroom_teacher_view_studenthub_dashboard.html", context)


@login_required
def classroom_teacher_student_subjects_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not verify_classroom_teacher_access(request.user, student):
        return render(request, "errors/403.html", status=403)
    context = build_student_subject_metadata_context(student)
    return render(request, "dashboards/classroom_teacher/classroom_teacher_view_subjects.html", context)


@login_required
def classroom_teacher_exam_results_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not verify_classroom_teacher_access(request.user, student):
        return render(request, "errors/403.html", status=403)
    context = get_exam_results_context(student)
    context.update(get_student_exam_highlights(student))
    context["student"] = student
    return render(request, "dashboards/classroom_teacher/classroom_teacher_view_exam_results.html", context)


@login_required
def classroom_teacher_exam_timetable_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not verify_classroom_teacher_access(request.user, student):
        return render(request, "errors/403.html", status=403)
    schedule = get_student_exam_schedule(student)
    context = {"student": student, "exams": schedule.get("exams", [])}
    return render(request, "dashboards/classroom_teacher/classroom_teacher_view_exam_timetable.html", context)


@login_required
def classroom_teacher_grade_insights_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not verify_classroom_teacher_access(request.user, student):
        return render(request, "errors/403.html", status=403)
    context = build_grade_insights_context(student)
    return render(request, "dashboards/classroom_teacher/classroom_teacher_view_grade_insights.html", context)


@login_required
def classroom_teacher_report_card_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not verify_classroom_teacher_access(request.user, student):
        return render(request, "errors/403.html", status=403)
    context = build_exam_report_context(student)
    return render(request, "dashboards/classroom_teacher/classroom_teacher_view_report_card.html", context)


@login_required
def classroom_teacher_printable_report_card(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not verify_classroom_teacher_access(request.user, student):
        return render(request, "errors/403.html", status=403)
    context = build_exam_report_context(student)
    return render(request, "pdf/_pdf_student_report.html", context)


@login_required
def classroom_teacher_performance_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not verify_classroom_teacher_access(request.user, student):
        return render(request, "errors/403.html", status=403)
    context = build_student_exam_performance_context(student)
    return render(request, "dashboards/classroom_teacher/classroom_teacher_view_performance.html", context)


@login_required
def classroom_teacher_subject_comments_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not verify_classroom_teacher_access(request.user, student):
        return render(request, "errors/403.html", status=403)
    context = build_student_subject_comments_context(student)
    return render(request, "dashboards/classroom_teacher/classroom_teacher_view_comments.html", context)


@login_required
def classroom_teacher_contact_teachers_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not verify_classroom_teacher_access(request.user, student):
        return render(request, "errors/403.html", status=403)
    context = build_student_teacher_contact_context(student)
    return render(request, "dashboards/classroom_teacher/classroom_teacher_view_contacts.html", context)


# ===============================
# Teacher Dashboards & Analytics
# ===============================

@login_required
def classroom_teacher_view_subject_performance(request):
    teacher = request.user.teacher
    context = get_subject_performance_context(teacher)
    return render(
        request,
        "dashboards/classroom_teacher/classroom_teacher_view_subject_performance.html",
        context
    )


@login_required
def classroom_teacher_view_student_view(request):
    context = get_student_card_context_for_teacher(request)
    return render(
        request,
        "dashboards/classroom_teacher/classroom_teacher_view_student.html",
        context
    )


@login_required
def classroom_teacher_student_charts_view(request):
    context = {
        "chart_data_list": get_chart_data_list_for_teacher(request)
    }
    return render(
        request,
        "dashboards/classroom_teacher/classroom_teacher_view_charts.html",
        context
    )
