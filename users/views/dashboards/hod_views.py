'''
users > views > dashboards > hod_views.py

Contains views accessible to HODs (Head of Departments).
'''

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

# Models
from users.models import Student
from the_school.models import Subject
from exams.models import StudentMark

# Context
from users.services.teacher_based_context.v2_subject_performance_context import get_subject_performance_context
from users.services.teacher_based_services.v2_student_card_service import get_students_for_teacher
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


# =====================================================
# 🧑‍🏫 HEAD OF DEPARTMENT (HOD) DASHBOARD VIEW
# =====================================================
@login_required
def hod_dashboard(request):
    return render(request, 'dashboards/hod_teacher/hod_teacher_dashboard.html')


# ========================================================
# 🏛️ HOD: Subject Performance View
# ========================================================
@login_required
def hod_view_subject_performance(request):
    teacher = request.user.teacher
    context = get_subject_performance_context(teacher)
    return render(request, "dashboards/hod_teacher/hod_view_subject_performance.html", context)


# ========================================================
# 🎓 HOD: Department Student List View
# ========================================================
@login_required
def hod_view_student_view(request):
    students = get_students_for_teacher(request.user)
    context = {"students": students}
    return render(request, "dashboards/hod_teacher/hod_view_student.html", context)


# ========================================================
# 🧠 HOD: Student Hub View (Entry Point)
# ========================================================
@login_required
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
    return render(
        request,
        "dashboards/hod_teacher/hod_view_studenthub_dashboard.html",
        context
    )


# ========================================================
# 📘 HOD: Shared Per-Student Subviews
# ========================================================

def verify_hod_access(user, student):
    teacher = getattr(user, "teacher", None)
    if not teacher:
        return False
    subject_ids = Subject.objects.filter(department__head_of_department=teacher).values_list("id", flat=True)
    return StudentMark.objects.filter(student=student, exam__subject_id__in=subject_ids).exists()


@login_required
def hod_student_subjects_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not verify_hod_access(request.user, student):
        return render(request, "errors/403.html", status=403)
    context = build_student_subject_metadata_context(student)
    return render(request, "dashboards/hod_teacher/hod_view_subjects.html", context)


@login_required
def hod_exam_results_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not verify_hod_access(request.user, student):
        return render(request, "errors/403.html", status=403)
    context = get_exam_results_context(student)
    context.update(get_student_exam_highlights(student))
    context["student"] = student
    return render(request, "dashboards/hod_teacher/hod_view_exam_results.html", context)


@login_required
def hod_exam_timetable_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not verify_hod_access(request.user, student):
        return render(request, "errors/403.html", status=403)
    schedule = get_student_exam_schedule(student)
    context = {"student": student, "exams": schedule.get("exams", [])}
    return render(request, "dashboards/hod_teacher/hod_view_exam_timetable.html", context)


@login_required
def hod_grade_insights_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not verify_hod_access(request.user, student):
        return render(request, "errors/403.html", status=403)
    context = build_grade_insights_context(student)
    return render(request, "dashboards/hod_teacher/hod_view_grade_insights.html", context)


@login_required
def hod_report_card_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not verify_hod_access(request.user, student):
        return render(request, "errors/403.html", status=403)
    context = build_exam_report_context(student)
    return render(request, "dashboards/hod_teacher/hod_view_report_card.html", context)


@login_required
def hod_printable_report_card(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not verify_hod_access(request.user, student):
        return render(request, "errors/403.html", status=403)
    context = build_exam_report_context(student)
    return render(request, "pdf/_pdf_student_report.html", context)


@login_required
def hod_performance_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not verify_hod_access(request.user, student):
        return render(request, "errors/403.html", status=403)
    context = build_student_exam_performance_context(student)
    return render(request, "dashboards/hod_teacher/hod_view_performance.html", context)


@login_required
def hod_subject_comments_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not verify_hod_access(request.user, student):
        return render(request, "errors/403.html", status=403)
    context = build_student_subject_comments_context(student)
    return render(request, "dashboards/hod_teacher/hod_view_comments.html", context)


@login_required
def hod_contact_teachers_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not verify_hod_access(request.user, student):
        return render(request, "errors/403.html", status=403)
    context = build_student_teacher_contact_context(student)
    return render(request, "dashboards/hod_teacher/hod_view_contacts.html", context)
