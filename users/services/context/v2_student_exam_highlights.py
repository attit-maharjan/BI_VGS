# ✅ users/services/context/v2_student_exam_highlights.py
from users.services.context.v2_student_exam_insights_context import get_report_card_context

def get_student_exam_highlights(student):
    """
    Returns lightweight exam highlight context useful for dashboard metrics and shared includes.
    Includes: GPA, average score, average grade, and academic year name.
    """
    rc = get_report_card_context(student)
    return {
        "overall": rc["overall"],
        "average_score": rc["average_score"],
        "average_grade": rc["average_grade"],
        "academic_year": rc["academic_year"]
    }
