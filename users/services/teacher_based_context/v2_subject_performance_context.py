"""
users > services > teacher_based_context > v2_subject_performance_context.py

This context builder loads role-aware subject lists using the helper
and applies subject performance analytics using the service.
It prepares a structured dictionary for rendering in templates.
"""

from users.helpers.teacher_based_helpers.v2_subject_performance_helper import get_subjects_for_teacher
from users.services.teacher_based_services.v2_subject_performance_service import calculate_subject_performance


def get_subject_performance_context(teacher):
    """
    Build context data for a given teacher based on their role.

    Parameters:
    - teacher (Teacher): The logged-in teacher instance

    Returns:
    - dict: Context containing subject analytics for templates
    """
    subjects = get_subjects_for_teacher(teacher)
    analytics_data = calculate_subject_performance(subjects)

    return {
        "subject_performance_analytics": analytics_data,
        "subject_count": subjects.count()
    }


def get_subject_performance_context_for_principal(teacher, request):
    """
    For Principal and Vice Principal — supports filtering by subject only (no teacher filter).
    """
    all_subjects = get_subjects_for_teacher(teacher)
    all_data = calculate_subject_performance(all_subjects)

    q_subject = request.GET.get("subject_id", "").strip()

    if q_subject:
        all_data = [
            item for item in all_data
            if str(item["subject"].id) == q_subject
        ]

    return {
        "subject_performance_analytics": all_data,
        "subject_count": len(all_data),
        "filter_subjects": all_subjects,
    }