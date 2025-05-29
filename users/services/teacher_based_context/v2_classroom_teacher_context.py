# v2_classroom_teacher_context.py

from users.services.teacher_based_services.v2_classroom_teacher_service import (
    fetch_classgroup_and_students_for_teacher
)

def classroom_teacher_dashboard_context(user):
    """
    Provides context for the classroom teacher dashboard.
    """
    return fetch_classgroup_and_students_for_teacher(user)
