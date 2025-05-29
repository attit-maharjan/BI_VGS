# users/views/dashboards/classroom_teacher_views.py
"""
users > views > dashboards > classroom_teacher_views.py

This file contains views accessible to classroom teachers.
Powered by reusable role-agnostic contexts.
"""



from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

# Models
from users.models import Student
from enrollments.models import ClassGroupStudentEnrollment

# Dashboard Context Services
from users.services.teacher_based_context.v2_classroom_teacher_context import classroom_teacher_dashboard_context
from users.services.teacher_based_context.v2_subject_assignment_context import classroom_teacher_subjects_context
from users.services.context.v2_student_dashboard_context import get_full_student_context

# Student Academic Context Services
from users.services.context.v2_student_metadata_context import build_student_subject_metadata_context
from users.services.context.v2_student_exam_insights_context import get_exam_results_context
from users.services.context.v2_student_grade_insights_context import build_grade_insights_context
from users.services.context.v2_exam_report_final_context import build_exam_report_context
from users.services.context.v2_student_exam_performance_context import build_student_exam_performance_context
from users.services.context.v2_1_student_subject_comments_context import build_student_subject_comments_context
from users.services.context.v2_student_teacher_contact_context import build_student_teacher_contact_context
from users.services.student_dashboard_service import get_student_exam_schedule

from users.services.context.v2_student_exam_highlights import get_student_exam_highlights

# ========================================================
# 🧑‍🏫 Classroom Teacher Dashboard View
# ========================================================
# This view renders the classroom teacher's dashboard.
# It displays their assigned class group and a list of 
# actively enrolled students within it.
# ========================================================

@login_required
def classroom_teacher_dashboard(request):
    context = classroom_teacher_dashboard_context(request.user)
    return render(
        request,
        "dashboards/classroom_teacher/classroom_teacher_dashboard.html",
        context
    )


# ========================================================
# 📚 Subject List View for Class Group
# ========================================================
# Shows all subjects assigned to the teacher's class group
# ========================================================

@login_required
def class_subjects_view(request):
    context = classroom_teacher_subjects_context(request.user)
    return render(
        request,
        "dashboards/classroom_teacher/class_student_subjects.html",
        context
    )


# ========================================================
# 🧑‍🎓 Per-Student Hub View
# ========================================================
# Renders a student dashboard wrapper view that includes
# the full hub UI for the selected student via a shared include.
# ========================================================

@login_required
def classroom_teacher_view_studenthub_dashboard(request, student_id):
    teacher = request.user.teacher
    classgroup_assignment = teacher.classgroup_assignments.filter(is_active=True).first()

    if not classgroup_assignment:
        return render(request, "errors/403.html", status=403)

    class_group = classgroup_assignment.class_group

    enrollment = get_object_or_404(
        ClassGroupStudentEnrollment,
        student_id=student_id,
        class_group=class_group,
        is_active=True
    )

    context = get_full_student_context(enrollment.student)
    return render(
        request,
        "dashboards/classroom_teacher/classroom_teacher_view_studenthub_dashboard.html",
        context
    )


# ========================================================
# 📘 Student Subviews (Shared Includes)
# ========================================================
# These views reuse shared includes and context services.
# ========================================================

def verify_classroom_teacher_access(user, student):
    teacher = getattr(user, "teacher", None)
    if not teacher:
        return False
    return ClassGroupStudentEnrollment.objects.filter(
        student=student,
        class_group__in=teacher.classgroup_assignments.values_list("class_group", flat=True),
        is_active=True
    ).exists()

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
    context = {
        "student": student,
        "exams": schedule.get("exams", [])
    }
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



from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Models
from users.models import Teacher

# Context
from users.services.teacher_based_context.v2_subject_performance_context import get_subject_performance_context


# ========================================================
# 📊 Classroom Teacher: Subject Performance View
# ========================================================
# Displays analytics for subjects taught in the teacher's classgroup.
# ========================================================

@login_required
def classroom_teacher_view_subject_performance(request):
    """
    View for classroom teachers to see subject performance for the class groups
    they are assigned to. Uses a role-aware, reusable context service.
    """
    teacher = request.user.teacher  # assumes OneToOne relation: User → Teacher
    context = get_subject_performance_context(teacher)
    return render(
        request,
        "dashboards/classroom_teacher/classroom_teacher_view_subject_performance.html",
        context
    )




# users/views/classroom_teacher_views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.services.teacher_based_services.v2_student_card_service import get_students_for_teacher

@login_required
def classroom_teacher_view_student_view(request):
    students = get_students_for_teacher(request.user)
    context = {
        "students": students,
    }
    return render(request, "dashboards/classroom_teacher/classroom_teacher_view_student.html", context)
