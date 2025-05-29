# users/services/context/parent_context_service.py

from users.services.parent_dashboard_service import get_students_under_parent
from users.services.context.v2_student_exam_insights_context import (
    get_report_card_context,
    get_exam_results_context,
    get_performance_context,
    get_grade_insights_context,
    get_comments_context
)

# ==============================================================================
# 🎯 ROLE-SPECIFIC CONTEXT FOR PARENT VIEWS
# ==============================================================================

def get_parent_dashboard_context(parent):
    """
    Builds a context for the main parent dashboard.
    Includes all children and a summarized dashboard per child.
    """
    students = get_students_under_parent(parent)
    children_dashboards = []

    for student in students:
        # Basic dashboard summary
        report_context = get_report_card_context(student)

        children_dashboards.append({
            "student": student,
            "dashboard": {
                "gpa": report_context["overall"]["gpa"] if report_context.get("overall") else None,
                "average_score": report_context.get("average_score"),
                "classgroup": {
                    "name": report_context.get("class_group"),
                    "academic_year": report_context.get("academic_year"),
                },
                "class_teacher_name": report_context.get("class_teacher_name"),
            }
        })

    return {
        "children_dashboards": children_dashboards
    }


def get_parent_child_full_context(student):
    """
    Full context for a single child's detailed dashboard view (as seen by the parent).
    Useful when a parent selects a specific child to view detailed performance.
    """
    return {
        "student": student,
        **get_report_card_context(student),
        **get_exam_results_context(student),
        **get_performance_context(student),
        **get_grade_insights_context(student),
        **get_comments_context(student),
    }
