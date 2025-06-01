# ---------------------------------------------
# 📄 Service: get_students_for_exam_update
# 🔹 Role: Subject Teacher
# 🔹 Purpose: Return students + marks linked to a given exam
# ---------------------------------------------

from exams.models import StudentMark
from enrollments.models import ClassGroupStudentEnrollment


def get_students_for_exam_update(exam):
    """
    Returns a queryset of StudentMark objects for students enrolled in the exam's class group.
    If a StudentMark doesn't exist, it creates one in memory (unsaved) for rendering purposes.
    """
    # Get all students enrolled in the exam's class group
    enrolled_students = ClassGroupStudentEnrollment.objects.filter(
        class_group=exam.class_group,
        is_active=True
    ).select_related('student')

    # Prefetch all existing marks for this exam
    existing_marks = StudentMark.objects.filter(exam=exam)
    marks_dict = {mark.student_id: mark for mark in existing_marks}

    student_marks = []

    # Ensure every enrolled student has a mark object (real or in-memory)
    for enrollment in enrolled_students:
        student = enrollment.student
        mark = marks_dict.get(student.id)

        if mark:
            student_marks.append(mark)
        else:
            student_marks.append(StudentMark(student=student, exam=exam))  # unsaved, blank form

    return student_marks
