from users.services.context.v2_student_grade_insights_context import build_grade_insights_context
from users.helpers.v2_generate_grade_distribution_charts import generate_grade_distribution_charts

def build_exam_report_context(student):
    """
    Safe, accurate report card context builder.
    Combines exam + mark + matching chart using exam.id-based mapping.
    Does NOT modify original chart generator logic.
    """
    # ✅ Use existing grade insights service for GPA, metadata
    context = build_grade_insights_context(student)

    # ✅ Use data we already know works
    exams = sorted({m.exam for m in student.exam_marks.select_related("exam").all()}, key=lambda x: x.date_conducted)
    class_group = context.get("classgroup")

    # ✅ Get charts (list format from original helper)
    charts_list = generate_grade_distribution_charts(student, exams, class_group)

    # ✅ Build a mapping: exam.id → chart HTML
    charts = {exam.id: charts_list[i] for i, exam in enumerate(exams) if i < len(charts_list)}

    # ✅ Assemble detailed exam_data rows
    exam_data = []
    for mark in student.exam_marks.select_related("exam").all():
        exam = mark.exam
        exam_data.append({
            "exam": exam,
            "mark": mark,
            "exam_code": f"{exam.subject.code}-{exam.exam_type.name[:3].upper()}",
            "chart_html": charts.get(exam.id, ""),
        })

    # ✅ Final context, enhanced
    context["exam_data"] = exam_data
    return context
