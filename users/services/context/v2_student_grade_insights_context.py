# v2_student_grade_insights_context.py
from exams.models import StudentMark
from users.models import Student
from enrollments.models import ClassGroupStudentEnrollment, ClassGroupTeacherAssignment
from users.helpers.v2_generate_grade_distribution_charts import (
    generate_grade_distribution_charts,
    compute_gpa_and_average_grade
)


def build_grade_insights_context(student):
    # 🔹 Get class group enrollment
    enrollment = ClassGroupStudentEnrollment.objects.select_related('class_group').filter(
        student=student, is_active=True
    ).first()
    class_group = enrollment.class_group if enrollment else None

    # 🔹 Get number of students in class
    student_count = ClassGroupStudentEnrollment.objects.filter(
        class_group=class_group, is_active=True
    ).count()

    # 🔹 Get class teacher (via assignment model)
    class_teacher_assignment = ClassGroupTeacherAssignment.objects.filter(
        class_group=class_group,
        is_active=True
    ).select_related('teacher__user').first()

    class_teacher_name = (
        class_teacher_assignment.teacher.user.get_full_name()
        if class_teacher_assignment and class_teacher_assignment.teacher and class_teacher_assignment.teacher.user
        else "Not Assigned"
    )

    # 🔹 Pull all student marks
    marks = StudentMark.objects.filter(student=student).select_related('exam')
    scores = [m.score for m in marks if m.score is not None]
    average_score = round(sum(scores) / len(scores), 2) if scores else 0

    # 🔹 Compute GPA + average grade + color (realistic)
    grade_result = compute_gpa_and_average_grade(marks)
    average_grade = grade_result.get('letter', 'N/A')
    gpa = grade_result.get('gpa', 0.0)
    grade_color = grade_result.get('grade_color', 'bg-gray-400')

    # 🔹 Exams (distinct, sorted)
    exams = sorted({m.exam for m in marks}, key=lambda x: x.date_conducted)

    # 🔹 Generate bar charts
    charts = generate_grade_distribution_charts(student, exams, class_group)

    # 🔹 Final context
    return {
        "student": student,
        "classgroup": class_group,
        "student_count": student_count,
        "class_teacher_name": class_teacher_name,
        "average_score": average_score,
        "gpa": gpa,
        "average_grade": average_grade,
        "average_grade_color": grade_color,
        "grade_distribution_charts": charts,
    }
