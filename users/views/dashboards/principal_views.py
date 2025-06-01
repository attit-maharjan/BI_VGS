'''
users > views > dashboards > principal_views.py

Contains all views accessible to the Principal role, structured to ensure school-wide access.
'''

# ===============================
# 📦 Django Core Imports
# ===============================
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

# ===============================
# 📘 Models
# ===============================
from users.models import Student

# ===============================
# 🧠 Services and Context Builders
# ===============================
from users.services.teacher_based_context.v2_subject_performance_context import (
    get_subject_performance_context_for_principal,
)
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

# ===============================
# 🏫 Principal: Dashboard Home
# ===============================
@login_required
def principal_dashboard(request):
    return render(request, 'dashboards/principal/principal_dashboard.html')


# ===============================
# 📊 Subject Performance
# ===============================
@login_required
def principal_view_subject_performance(request):
    teacher = request.user.teacher
    context = get_subject_performance_context_for_principal(teacher, request)
    return render(request, "dashboards/principal/principal_view_subject_performance.html", context)


# ===============================
# 👥 View All Students
# ===============================
@login_required
def principal_view_student_view(request):
    context = get_student_card_context_for_teacher(request)
    return render(request, "dashboards/principal/principal_view_student.html", context)


# ===============================
# 🧠 Student Hub
# ===============================
@login_required
def principal_view_studenthub_dashboard(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    context = get_full_student_context(student)
    return render(request, "dashboards/principal/principal_view_studenthub_dashboard.html", context)


# ===============================
# 📘 Shared Subviews
# ===============================
@login_required
def principal_student_subjects_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    context = build_student_subject_metadata_context(student)
    return render(request, "dashboards/principal/principal_view_subjects.html", context)


@login_required
def principal_exam_results_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    context = get_exam_results_context(student)
    context.update(get_student_exam_highlights(student))
    context["student"] = student
    return render(request, "dashboards/principal/principal_view_exam_results.html", context)


@login_required
def principal_exam_timetable_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    schedule = get_student_exam_schedule(student)
    context = {"student": student, "exams": schedule.get("exams", [])}
    return render(request, "dashboards/principal/principal_view_exam_timetable.html", context)


@login_required
def principal_grade_insights_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    context = build_grade_insights_context(student)
    return render(request, "dashboards/principal/principal_view_grade_insights.html", context)


@login_required
def principal_report_card_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    context = build_exam_report_context(student)
    return render(request, "dashboards/principal/principal_view_report_card.html", context)


@login_required
def principal_printable_report_card(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    context = build_exam_report_context(student)
    return render(request, "pdf/_pdf_student_report.html", context)


@login_required
def principal_performance_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    context = build_student_exam_performance_context(student)
    return render(request, "dashboards/principal/principal_view_performance.html", context)


@login_required
def principal_subject_comments_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    context = build_student_subject_comments_context(student)
    return render(request, "dashboards/principal/principal_view_comments.html", context)


@login_required
def principal_contact_teachers_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    context = build_student_teacher_contact_context(student)
    return render(request, "dashboards/principal/principal_view_contacts.html", context)


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from users.services.teacher_based_services.student_performance_chart_service import get_chart_data_list_for_teacher
from users.services.teacher_based_context.chart_filter_context import get_chart_filter_context

@login_required
def principal_student_charts_view(request):
    context = {
        "chart_data_list": get_chart_data_list_for_teacher(request),
        **get_chart_filter_context(request)
    }
    return render(
        request,
        "dashboards/principal/principal_view_charts.html",
        context
    )
