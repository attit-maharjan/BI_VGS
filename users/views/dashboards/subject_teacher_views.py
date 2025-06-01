"""
users > views > dashboards > subject_teacher_views.py

This file contains all Subject Teacher dashboard views.
Views are grouped by purpose and documented clearly.
All views rely on shared includes and role-based access checks.
"""

# ===============================
# 📦 Django Core
# ===============================
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

# ===============================
# 📘 Models
# ===============================
from users.models import Student
from enrollments.models import TeacherSubjectAssignment
from exams.models import StudentMark

# ===============================
# 🧠 Context Services
# ===============================
from users.services.teacher_based_services.v2_student_card_service import get_student_card_context_for_teacher
from users.services.teacher_based_context.v2_subject_performance_context import get_subject_performance_context
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
# 🔐 Access Control
# ===============================
def verify_subject_teacher_access(user, student):
    teacher = getattr(user, "teacher", None)
    if not teacher:
        return False

    assigned_subject_ids = TeacherSubjectAssignment.objects.filter(
        teacher=teacher, is_active=True
    ).values_list("subject_id", flat=True)

    return StudentMark.objects.filter(
        student=student,
        exam__subject_id__in=assigned_subject_ids
    ).exists()


# ===============================
# 🧑‍🏫 Dashboard Views
# ===============================
@login_required
def subject_teacher_dashboard(request):
    return render(request, "dashboards/subject_teacher/subject_teacher_dashboard.html")


@login_required
def subject_teacher_view_subject_performance(request):
    teacher = request.user.teacher
    context = get_subject_performance_context(teacher)
    return render(
        request,
        "dashboards/subject_teacher/subject_teacher_view_subject_performance.html",
        context
    )


@login_required
def subject_teacher_view_student_view(request):
    context = get_student_card_context_for_teacher(request)
    return render(
        request,
        "dashboards/subject_teacher/subject_teacher_view_student.html",
        context
    )


@login_required
def subject_teacher_view_studenthub_dashboard(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not verify_subject_teacher_access(request.user, student):
        return render(request, "errors/403.html", status=403)

    context = get_full_student_context(student)
    return render(
        request,
        "dashboards/subject_teacher/subject_teacher_view_studenthub_dashboard.html",
        context
    )


# ===============================
# 📘 Student Subviews
# ===============================
@login_required
def subject_teacher_student_subjects_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not verify_subject_teacher_access(request.user, student):
        return render(request, "errors/403.html", status=403)

    context = build_student_subject_metadata_context(student)
    return render(request, "dashboards/subject_teacher/subject_teacher_view_subjects.html", context)


@login_required
def subject_teacher_exam_results_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not verify_subject_teacher_access(request.user, student):
        return render(request, "errors/403.html", status=403)

    context = get_exam_results_context(student)
    context.update(get_student_exam_highlights(student))
    context["student"] = student
    return render(request, "dashboards/subject_teacher/subject_teacher_view_exam_results.html", context)


@login_required
def subject_teacher_exam_timetable_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not verify_subject_teacher_access(request.user, student):
        return render(request, "errors/403.html", status=403)

    schedule = get_student_exam_schedule(student)
    return render(request, "dashboards/subject_teacher/subject_teacher_view_exam_timetable.html", {
        "student": student,
        "exams": schedule.get("exams", [])
    })


@login_required
def subject_teacher_grade_insights_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not verify_subject_teacher_access(request.user, student):
        return render(request, "errors/403.html", status=403)

    context = build_grade_insights_context(student)
    return render(request, "dashboards/subject_teacher/subject_teacher_view_grade_insights.html", context)


@login_required
def subject_teacher_report_card_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not verify_subject_teacher_access(request.user, student):
        return render(request, "errors/403.html", status=403)

    context = build_exam_report_context(student)
    return render(request, "dashboards/subject_teacher/subject_teacher_view_report_card.html", context)


@login_required
def subject_teacher_printable_report_card(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not verify_subject_teacher_access(request.user, student):
        return render(request, "errors/403.html", status=403)

    context = build_exam_report_context(student)
    return render(request, "pdf/_pdf_student_report.html", context)


@login_required
def subject_teacher_performance_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not verify_subject_teacher_access(request.user, student):
        return render(request, "errors/403.html", status=403)

    context = build_student_exam_performance_context(student)
    return render(request, "dashboards/subject_teacher/subject_teacher_view_performance.html", context)


@login_required
def subject_teacher_subject_comments_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not verify_subject_teacher_access(request.user, student):
        return render(request, "errors/403.html", status=403)

    context = build_student_subject_comments_context(student)
    return render(request, "dashboards/subject_teacher/subject_teacher_view_comments.html", context)


@login_required
def subject_teacher_contact_teachers_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not verify_subject_teacher_access(request.user, student):
        return render(request, "errors/403.html", status=403)

    context = build_student_teacher_contact_context(student)
    return render(request, "dashboards/subject_teacher/subject_teacher_view_contacts.html", context)



from users.services.teacher_based_services.student_performance_chart_service import get_chart_data_list_for_teacher

@login_required
def subject_teacher_student_charts_view(request):
    context = {
        "chart_data_list": get_chart_data_list_for_teacher(request)
    }
    return render(
        request,
        "dashboards/subject_teacher/subject_teacher_view_charts.html",
        context
    )
    
    
    
    
# ---------------------------------------------
# 📄 View: update_exam_marks_view
# 🔹 Role: Subject Teacher
# 🔹 Purpose: Render and process mark update form for a specific exam
# ---------------------------------------------
# ✅ File: users/views/dashboards/subject_teacher_views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from exams.models import Exam, StudentMark
from users.forms_crud_transactions.update_exam_marks import UpdateStudentMarksFormSet
from users.helpers.teacher_based_helpers.subject_teacher_access_control import validate_subject_teacher_access
from users.services.teacher_based_services.subject_teacher_exam_service import get_students_for_exam_update


def update_exam_marks_view(request, exam_id):
    # Retrieve the exam instance based on the provided ID
    exam = get_object_or_404(Exam, id=exam_id)

    # Ensure the logged-in teacher is authorized to access this subject
    validate_subject_teacher_access(request.user, exam.subject)

    # Get list of StudentMark instances (real or unsaved)
    student_marks = get_students_for_exam_update(exam)

    if request.method == 'POST':
        formset = UpdateStudentMarksFormSet(request.POST)
        for form, mark in zip(formset.forms, student_marks):
            form.instance = mark

        if formset.is_valid():
            updated_count = 0
            for form in formset:
                mark_obj = form.save(commit=False)
                if 'score' in form.changed_data:
                    mark_obj.exam = exam
                    mark_obj.save()
                    updated_count += 1

            messages.success(request, f"Updated marks for {updated_count} student(s).")
            return redirect('users:update_exam_marks', exam_id=exam.id)
        else:
            messages.error(request, "There was an error in the form. Please correct the marked fields.")
    else:
        initial_data = [{'score': mark.score} for mark in student_marks]
        formset = UpdateStudentMarksFormSet(initial=initial_data)
        for form, mark in zip(formset.forms, student_marks):
            form.instance = mark

    return render(request, 'dashboards/subject_teacher/crud_transactions/update_exam_marks.html', {
        'exam': exam,
        'formset': formset,
    })
