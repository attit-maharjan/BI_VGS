# ==============================================================================
# 🌐 PARENT VIEWS - BIVGS DASHBOARD
# Path: users/views/dashboards/parent_views.py
# ------------------------------------------------------------------------------
# This file contains all view functions associated with the Parent role:
# - Main Parent Dashboard: lists their children
# - Per-child dashboards: subjects, exams, insights, performance, comments
# - Reuses shared context services (v2_*) and shared includes
# 
# Context Services Used:
# - v2_student_dashboard_context.py
# - v2_student_metadata_context.py
# - v2_student_exam_insights_context.py
# - v2_student_grade_insights_context.py
# - v2_exam_report_final_context.py
# - v2_student_exam_performance_context.py
# - v2_1_student_subject_comments_context.py
# - v2_student_teacher_contact_context.py
# ==============================================================================

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from users.shared_utilities.decorators import parent_required

# Models
from users.models import Student

# Core context services
from users.services.parent_dashboard_service import get_students_under_parent
from users.services.context.v2_student_dashboard_context import (
    get_full_student_context,
    get_classgroup_for_student
)
from users.services.context.v2_student_exam_insights_context import get_exam_results_context
from users.services.context.v2_student_exam_highlights import get_student_exam_highlights
from users.services.context.v2_student_metadata_context import build_student_subject_metadata_context
from users.services.context.v2_student_grade_insights_context import build_grade_insights_context
from users.services.context.v2_exam_report_final_context import build_exam_report_context
from users.services.context.v2_student_exam_performance_context import build_student_exam_performance_context
from users.services.context.v2_1_student_subject_comments_context import build_student_subject_comments_context
from users.services.context.v2_student_teacher_contact_context import build_student_teacher_contact_context

# ==============================================================================
# 🏠 MAIN PARENT DASHBOARD (Lists Children)
# ==============================================================================

@login_required
@parent_required
def parent_dashboard(request):
    parent = request.user.parent
    students = get_students_under_parent(parent)

    children_dashboards = [get_full_student_context(s) for s in students]

    context = {
        "children_dashboards": children_dashboards,
        "child_count": len(students),
        "child_names": [s.user.get_full_name() for s in students],
        "current_year": get_classgroup_for_student(students[0]).academic_year if students else None,
        "hide_sidebar_nav": True,  # Hide sidebar before a specific child is selected
    }

    return render(request, "dashboards/parent/parent_dashboard.html", context)

# ==============================================================================
# 👤 PER-CHILD DASHBOARD HUB
# ==============================================================================

@login_required
@parent_required
def parent_child_dashboard_view(request, student_id):
    parent = request.user.parent
    student = get_object_or_404(Student, id=student_id)

    if student.father != parent and student.mother != parent and student.guardian != parent:
        return render(request, "errors/403.html", status=403)

    context = get_full_student_context(student)
    return render(request, "dashboards/parent/parent_view_childhub_dashboard.html", context)

# ==============================================================================
# 📚 PER-CHILD SUBJECTS & TEACHERS VIEW
# ==============================================================================

@login_required
@parent_required
def parent_child_subjects_view(request, student_id):
    parent = request.user.parent
    student = get_object_or_404(Student, id=student_id)

    if student.father != parent and student.mother != parent and student.guardian != parent:
        return render(request, "errors/403.html", status=403)

    context = build_student_subject_metadata_context(student)
    return render(request, "dashboards/parent/parent_view_child_subjects.html", context)

# ==============================================================================
# 📝 PER-CHILD EXAM RESULTS VIEW
# ==============================================================================

@login_required
@parent_required
def parent_child_exam_results_view(request, student_id):
    parent = request.user.parent
    student = get_object_or_404(Student, id=student_id)

    if student.father != parent and student.mother != parent and student.guardian != parent:
        return render(request, "errors/403.html", status=403)

    context = get_exam_results_context(student)
    context.update(get_student_exam_highlights(student))
    context["student"] = student

    return render(request, "dashboards/parent/my_child_exam_results.html", context)

# ==============================================================================
# 🗓️ PER-CHILD EXAM TIMETABLE VIEW
# ==============================================================================

@login_required
@parent_required
def parent_child_exam_timetable_view(request, student_id):
    from users.services.student_dashboard_service import get_student_exam_schedule

    parent = request.user.parent
    student = get_object_or_404(Student, id=student_id)

    if student.father != parent and student.mother != parent and student.guardian != parent:
        return render(request, "errors/403.html", status=403)

    schedule = get_student_exam_schedule(student)

    context = {
        "student": student,
        "exams": schedule.get("exams", [])
    }

    return render(request, "dashboards/parent/my_child_exam_timetable.html", context)

# ==============================================================================
# 🧠 PER-CHILD GRADE INSIGHTS VIEW
# ==============================================================================

@login_required
@parent_required
def parent_child_grade_insights_view(request, student_id):
    parent = request.user.parent
    student = get_object_or_404(Student, id=student_id)

    if student.father != parent and student.mother != parent and student.guardian != parent:
        return render(request, "errors/403.html", status=403)

    context = build_grade_insights_context(student)
    return render(request, "dashboards/parent/my_child_grade_insights.html", context)

# ==============================================================================
# 🧾 REPORT CARD (HTML View)
# ==============================================================================

@login_required
@parent_required
def parent_child_report_card_view(request, student_id):
    parent = request.user.parent
    student = get_object_or_404(Student, id=student_id)

    if student.father != parent and student.mother != parent and student.guardian != parent:
        return render(request, "errors/403.html", status=403)

    context = build_exam_report_context(student)
    return render(request, "dashboards/parent/my_child_report_card.html", context)

# ==============================================================================
# 🧾 REPORT CARD (Printable PDF View)
# ==============================================================================

@login_required
@parent_required
def parent_printable_report_card(request, student_id):
    parent = request.user.parent
    student = get_object_or_404(Student, id=student_id)

    if student.father != parent and student.mother != parent and student.guardian != parent:
        return render(request, "errors/403.html", status=403)

    context = build_exam_report_context(student)
    return render(request, "pdf/_pdf_student_report.html", context)

# ==============================================================================
# 📊 PERFORMANCE COMPARISON VIEW
# ==============================================================================

@login_required
@parent_required
def parent_child_performance_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    context = build_student_exam_performance_context(student)
    return render(request, "dashboards/parent/my_child_exam_performance.html", context)

# ==============================================================================
# 💬 SUBJECT COMMENTS VIEW
# ==============================================================================

@login_required
@parent_required
def parent_subject_comments_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    context = build_student_subject_comments_context(student)
    return render(request, "dashboards/parent/my_child_subject_comments.html", context)

# ==============================================================================
# 📬 TEACHER CONTACTS VIEW
# ==============================================================================

@login_required
@parent_required
def parent_contact_teachers_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    context = build_student_teacher_contact_context(student)
    return render(request, "dashboards/parent/my_child_teacher_contacts.html", context)
