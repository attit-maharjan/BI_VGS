# users/helpers/teacher_based_helpers/v2_subject_assignment_helper.py

from enrollments.models import ClassGroupSubjectAssignment

def get_subjects_for_classgroup(class_group):
    """
    Returns all active subjects assigned to a class group
    for the group's academic year.
    """
    if not class_group or not class_group.academic_year:
        return []

    return (
        ClassGroupSubjectAssignment.objects
        .filter(
            class_group=class_group,
            academic_year=class_group.academic_year,
            is_active=True
        )
        .select_related("subject__department")
        .order_by("subject__name")
    )
