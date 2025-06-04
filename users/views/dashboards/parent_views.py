"""
users > views > dashboards > parent_views.py

Views for the Parent role in BIVGS. Handles:
- Main dashboard listing children
- Per-child academic dashboards
- Subject, exam, performance, and contact info

All views rely on shared context services and enforce strict access control to linked students.
"""

# ===============================
# 📦 Django Core & Decorators
# ===============================
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

# ===============================
# 🔒 Access Control
# ===============================
from users.shared_utilities.decorators import parent_required

# ===============================
# 📘 Models
# ===============================
from users.models import Student

# ===============================
# 🧠 Context Services
# ===============================
from users.services.parent_dashboard_service import get_students_under_parent
from users.services.context.v2_student_dashboard_context import get_full_student_context, get_classgroup_for_student
from users.services.context.v2_student_exam_insights_context import get_exam_results_context
from users.services.context.v2_student_exam_highlights import get_student_exam_highlights
from users.services.context.v2_student_metadata_context import build_student_subject_metadata_context
from users.services.context.v2_student_grade_insights_context import build_grade_insights_context
from users.services.context.v2_exam_report_final_context import build_exam_report_context
from users.services.context.v2_student_exam_performance_context import build_student_exam_performance_context
from users.services.context.v2_1_student_subject_comments_context import build_student_subject_comments_context
from users.services.context.v2_student_teacher_contact_context import build_student_teacher_contact_context
from users.services.student_dashboard_service import get_student_exam_schedule

# ===============================
# 🏠 Main Parent Dashboard
# ===============================
@login_required
@parent_required
def parent_dashboard(request):
    parent = request.user.parent
    students = get_students_under_parent(parent)

    context = {
        "children_dashboards": [get_full_student_context(s) for s in students],
        "child_count": len(students),
        "child_names": [s.user.get_full_name() for s in students],
        "current_year": get_classgroup_for_student(students[0]).academic_year if students else None,
        "hide_sidebar_nav": True,
    }
    return render(request, "dashboards/parent/parent_dashboard.html", context)

# ===============================
# 👤 Per-Child Dashboard View
# ===============================
@login_required
@parent_required
def parent_child_dashboard_view(request, student_id):
    parent = request.user.parent
    student = get_object_or_404(Student, id=student_id)

    if student.father != parent and student.mother != parent and student.guardian != parent:
        return render(request, "errors/403.html", status=403)

    context = get_full_student_context(student)
    return render(request, "dashboards/parent/parent_view_childhub_dashboard.html", context)

# ===============================
# 📚 Subjects & Teachers
# ===============================
@login_required
@parent_required
def parent_child_subjects_view(request, student_id):
    parent = request.user.parent
    student = get_object_or_404(Student, id=student_id)

    if student.father != parent and student.mother != parent and student.guardian != parent:
        return render(request, "errors/403.html", status=403)

    context = build_student_subject_metadata_context(student)
    return render(request, "dashboards/parent/parent_view_child_subjects.html", context)

# ===============================
# 📝 Exam Results
# ===============================
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

# ===============================
# 🗓️ Exam Timetable
# ===============================
@login_required
@parent_required
def parent_child_exam_timetable_view(request, student_id):
    parent = request.user.parent
    student = get_object_or_404(Student, id=student_id)

    if student.father != parent and student.mother != parent and student.guardian != parent:
        return render(request, "errors/403.html", status=403)

    schedule = get_student_exam_schedule(student)
    context = {"student": student, "exams": schedule.get("exams", [])}
    return render(request, "dashboards/parent/my_child_exam_timetable.html", context)

# ===============================
# 🧠 Grade Insights
# ===============================
@login_required
@parent_required
def parent_child_grade_insights_view(request, student_id):
    parent = request.user.parent
    student = get_object_or_404(Student, id=student_id)

    if student.father != parent and student.mother != parent and student.guardian != parent:
        return render(request, "errors/403.html", status=403)

    context = build_grade_insights_context(student)
    return render(request, "dashboards/parent/my_child_grade_insights.html", context)

# ===============================
# 🧾 Report Card (HTML)
# ===============================
@login_required
@parent_required
def parent_child_report_card_view(request, student_id):
    parent = request.user.parent
    student = get_object_or_404(Student, id=student_id)

    if student.father != parent and student.mother != parent and student.guardian != parent:
        return render(request, "errors/403.html", status=403)

    context = build_exam_report_context(student)
    return render(request, "dashboards/parent/my_child_report_card.html", context)

# ===============================
# 🧾 Report Card (PDF)
# ===============================
@login_required
@parent_required
def parent_printable_report_card(request, student_id):
    parent = request.user.parent
    student = get_object_or_404(Student, id=student_id)

    if student.father != parent and student.mother != parent and student.guardian != parent:
        return render(request, "errors/403.html", status=403)

    context = build_exam_report_context(student)
    return render(request, "pdf/_pdf_student_report.html", context)

# ===============================
# 📊 Performance Chart
# ===============================
@login_required
@parent_required
def parent_child_performance_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    context = build_student_exam_performance_context(student)
    return render(request, "dashboards/parent/my_child_exam_performance.html", context)

# ===============================
# 💬 Subject Comments
# ===============================
@login_required
@parent_required
def parent_subject_comments_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    context = build_student_subject_comments_context(student)
    return render(request, "dashboards/parent/my_child_subject_comments.html", context)

# ===============================
# 📬 Teacher Contacts
# ===============================
@login_required
@parent_required
def parent_contact_teachers_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    context = build_student_teacher_contact_context(student)
    return render(request, "dashboards/parent/my_child_teacher_contacts.html", context)
