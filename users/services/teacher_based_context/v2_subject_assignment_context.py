# users/services/teacher_based_context/v2_subject_assignment_context.py

from users.services.teacher_based_services.v2_subject_assignment_service import get_classgroup_subject_list

def classroom_teacher_subjects_context(user):
    """
    Provides context for the classroom teacher's subject list view.
    """
    return get_classgroup_subject_list(user)
