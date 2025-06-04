"""
users > views > dashboards > vice_principal_views.py

Views specific to Vice Principals: includes dashboards,
subject performance, student profiles, and analytics.
"""

# ===============================
# 📦 Django Core Imports
# ===============================
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

# ===============================
# 🧠 Models
# ===============================
from users.models import Student
from enrollments.models import ClassGroupStudentEnrollment

# ===============================
# 📊 Context & Service Layers
# ===============================
from users.services.student_dashboard_service import get_student_exam_schedule
from users.services.teacher_based_services.v2_student_card_service import (
    get_students_for_teacher,
    get_student_card_context_for_teacher,
)
from users.services.teacher_based_services.student_performance_chart_service import (
    get_chart_data_list_for_teacher,
)
from users.services.teacher_based_context.v2_subject_performance_context import (
    get_subject_performance_context_for_principal,
)
from users.services.teacher_based_context.chart_filter_context import (
    get_chart_filter_context,
)
from users.services.context.v2_student_dashboard_context import get_full_student_context
from users.services.context.v2_student_metadata_context import build_student_subject_metadata_context
from users.services.context.v2_student_exam_insights_context import get_exam_results_context
from users.services.context.v2_student_exam_highlights import get_student_exam_highlights
from users.services.context.v2_student_grade_insights_context import build_grade_insights_context
from users.services.context.v2_exam_report_final_context import build_exam_report_context
from users.services.context.v2_student_exam_performance_context import build_student_exam_performance_context
from users.services.context.v2_1_student_subject_comments_context import build_student_subject_comments_context
from users.services.context.v2_student_teacher_contact_context import build_student_teacher_contact_context


@login_required
def vice_principal_dashboard(request):
    return render(request, 'dashboards/vice_principal/vice_principal_dashboard.html')


@login_required
def vice_principal_view_subject_performance(request):
    teacher = request.user.teacher
    context = get_subject_performance_context_for_principal(teacher, request)
    return render(request, "dashboards/vice_principal/vice_principal_view_subject_performance.html", context)


@login_required
def vice_principal_view_student_view(request):
    context = get_student_card_context_for_teacher(request)
    if not context.get("students"):
        messages.warning(request, "No students found. They might not be assigned or enrolled yet.")
        return redirect("users:student_not_enrolled")
    return render(
        request,
        "dashboards/vice_principal/vice_principal_view_student.html",
        context
    )


@login_required
def vice_principal_view_studenthub_dashboard(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not ClassGroupStudentEnrollment.objects.filter(student=student).exists():
        messages.warning(request, "This student may not yet be enrolled in any class group.")
        return redirect("users:student_not_enrolled")
    context = get_full_student_context(student)
    return render(
        request,
        "dashboards/vice_principal/vice_principal_view_studenthub_dashboard.html",
        context
    )


@login_required
def vice_principal_student_subjects_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not ClassGroupStudentEnrollment.objects.filter(student=student).exists():
        messages.warning(request, "Student not enrolled in any class group.")
        return redirect("users:student_not_enrolled")
    context = build_student_subject_metadata_context(student)
    return render(request, "dashboards/vice_principal/vice_principal_view_subjects.html", context)


@login_required
def vice_principal_exam_results_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not ClassGroupStudentEnrollment.objects.filter(student=student).exists():
        messages.warning(request, "Student is not enrolled in any class group or has no exam results.")
        return redirect("users:student_not_enrolled")
    context = get_exam_results_context(student)
    context.update(get_student_exam_highlights(student))
    context["student"] = student
    return render(request, "dashboards/vice_principal/vice_principal_view_exam_results.html", context)


@login_required
def vice_principal_exam_timetable_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not ClassGroupStudentEnrollment.objects.filter(student=student).exists():
        messages.warning(request, "Student not enrolled. Cannot fetch timetable.")
        return redirect("users:student_not_enrolled")
    schedule = get_student_exam_schedule(student)
    context = {"student": student, "exams": schedule.get("exams", [])}
    return render(request, "dashboards/vice_principal/vice_principal_view_exam_timetable.html", context)


@login_required
def vice_principal_grade_insights_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not ClassGroupStudentEnrollment.objects.filter(student=student).exists():
        messages.warning(request, "Grade insights unavailable. Student not enrolled.")
        return redirect("users:student_not_enrolled")
    context = build_grade_insights_context(student)
    return render(request, "dashboards/vice_principal/vice_principal_view_grade_insights.html", context)


@login_required
def vice_principal_report_card_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not ClassGroupStudentEnrollment.objects.filter(student=student).exists():
        messages.warning(request, "Report card unavailable. Student not enrolled or has no exams.")
        return redirect("users:student_not_enrolled")
    try:
        context = build_exam_report_context(student)
    except Exception:
        messages.error(request, "Could not load report card. Data may be incomplete.")
        return redirect("users:student_not_enrolled")
    return render(request, "dashboards/vice_principal/vice_principal_view_report_card.html", context)


@login_required
def vice_principal_printable_report_card(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not ClassGroupStudentEnrollment.objects.filter(student=student).exists():
        messages.warning(request, "Printable report unavailable. Student not enrolled.")
        return redirect("users:student_not_enrolled")
    context = build_exam_report_context(student)
    return render(request, "pdf/_pdf_student_report.html", context)


@login_required
def vice_principal_performance_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not ClassGroupStudentEnrollment.objects.filter(student=student).exists():
        messages.warning(request, "No performance data. Student not enrolled.")
        return redirect("users:student_not_enrolled")
    context = build_student_exam_performance_context(student)
    return render(request, "dashboards/vice_principal/vice_principal_view_performance.html", context)


@login_required
def vice_principal_subject_comments_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not ClassGroupStudentEnrollment.objects.filter(student=student).exists():
        messages.warning(request, "Subject comments unavailable. Student not enrolled.")
        return redirect("users:student_not_enrolled")
    try:
        context = build_student_subject_comments_context(student)
    except Exception:
        messages.info(request, "No subject comments found for this student.")
        return redirect("users:student_not_enrolled")
    return render(request, "dashboards/vice_principal/vice_principal_view_comments.html", context)


@login_required
def vice_principal_contact_teachers_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not ClassGroupStudentEnrollment.objects.filter(student=student).exists():
        messages.warning(request, "Contact information unavailable. Student not enrolled.")
        return redirect("users:student_not_enrolled")
    context = build_student_teacher_contact_context(student)
    return render(request, "dashboards/vice_principal/vice_principal_view_contacts.html", context)




def vice_principal_student_charts_view(request):
    context = get_chart_filter_context(request)
    context["chart_data_list"] = get_chart_data_list_for_teacher(request)
    return render(request, "dashboards/vice_principal/vice_principal_view_charts.html", context)
