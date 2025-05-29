# v2_student_exam_performance_context.py

from exams.models import Exam, StudentMark
from users.services.context.v2_student_metadata_context import get_classgroup_for_student
from users.services.context.v2_student_grade_insights_context import build_grade_insights_context
from users.models import Student
from enrollments.models import ClassGroupStudentEnrollment
from the_school.models import Subject
from django.db.models import Avg
import plotly.graph_objects as go

def build_student_exam_performance_context(student):
    classgroup = get_classgroup_for_student(student)
    grade_level = classgroup.grade_level
    academic_year = classgroup.academic_year

    valid_subjects = Subject.objects.filter(grade_level=grade_level)
    exams = Exam.objects.filter(subject__in=valid_subjects, academic_year=academic_year)

    student_marks_qs = StudentMark.objects.filter(student=student, exam__in=exams)
    student_marks = {mark.exam_id: mark.score for mark in student_marks_qs}

    student_ids = ClassGroupStudentEnrollment.objects.filter(
        class_group=classgroup
    ).values_list("student_id", flat=True)

    for exam in exams:
        exam.class_avg = StudentMark.objects.filter(
            student__in=student_ids,
            exam=exam
        ).aggregate(avg=Avg("score"))["avg"] or 0

    exam_labels = [exam.exam_code for exam in exams]
    student_scores = [student_marks.get(exam.id, 0) for exam in exams]
    class_avg_scores = [exam.class_avg for exam in exams]

    bar_chart = go.Figure(data=[
        go.Bar(name='Student', x=exam_labels, y=student_scores),
        go.Bar(name='Class Average', x=exam_labels, y=class_avg_scores)
    ])
    bar_chart.update_layout(barmode='group')
    bar_chart_json = bar_chart.to_html(full_html=False)

    line_chart = go.Figure()
    line_chart.add_trace(go.Scatter(x=exam_labels, y=student_scores, mode='lines+markers', name='Student'))
    line_chart.add_trace(go.Scatter(x=exam_labels, y=class_avg_scores, mode='lines+markers', name='Class Average'))
    line_chart.update_layout(title='Performance Over Time', xaxis_title='Exam Code', yaxis_title='Score')
    line_chart_json = line_chart.to_html(full_html=False)

    # Reuse grade insights for GPA, avg score, avg grade
    grade_context = build_grade_insights_context(student)

    return {
        "student": student,
        "classgroup": classgroup,
        "exams": exams,
        "student_marks": student_marks,
        "bar_chart_json": bar_chart_json,
        "line_chart_json": line_chart_json,
        "average_score": grade_context["average_score"],
        "average_grade": grade_context["average_grade"],
        "average_grade_color": grade_context["average_grade_color"],
        "gpa": grade_context["gpa"],
    }
