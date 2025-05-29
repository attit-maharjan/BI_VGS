# ============================================================
# ✅ v2_student_dashboard_context.py
# ------------------------------------------------------------
# Student metadata and insight context builder.
# Modular, role-agnostic, scalable for parent, teacher, admin views.
# ============================================================

from users.services.context.v2_student_metadata_context import (
    get_classgroup_for_student,
    get_class_teacher_for_student,
    get_subjects_for_student,
    get_subjects_with_teachers_for_student
)
from users.services.context.v2_student_exam_insights_context import (
    get_report_card_context,
    get_exam_results_context,
    get_performance_context,
    get_grade_insights_context,
    get_comments_context,
)

# ------------------------------------------------------------------------------
# 🔁 Used by Parent role
# ------------------------------------------------------------------------------
def get_full_student_context(student):
    """
    Returns a unified context with both metadata and insights for one student.
    Suitable for parent, student, teacher views.
    """
    metadata = {
        "class_group": get_classgroup_for_student(student),
        "class_teacher": get_class_teacher_for_student(student),
        "subjects": get_subjects_for_student(student),
        "subjects_with_teachers": get_subjects_with_teachers_for_student(student),
    }

    insights = {
        "report_card": get_report_card_context(student),
        "exam_results": get_exam_results_context(student),
        "performance": get_performance_context(student),
        "grade_insights": get_grade_insights_context(student),
        "comments": get_comments_context(student),
    }

    return {
        "student": student,
        "metadata": metadata,
        "insights": insights
    }


