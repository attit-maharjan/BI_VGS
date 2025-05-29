# users/services/teacher_based_services/v2_subject_assignment_service.py

from users.helpers.teacher_based_helpers.v2_classroom_teacher_helper import get_assigned_classgroup
from users.helpers.teacher_based_helpers.v2_subject_assignment_helper import get_subjects_for_classgroup

def get_classgroup_subject_list(user):
    """
    Returns the class group and its subject assignments for a given teacher.
    """
    assignment = get_assigned_classgroup(user)
    if not assignment:
        return {"class_group": None, "subjects": []}

    class_group = assignment.class_group
    subjects = get_subjects_for_classgroup(class_group)

    return {
        "class_group": class_group,
        "subjects": subjects
    }
