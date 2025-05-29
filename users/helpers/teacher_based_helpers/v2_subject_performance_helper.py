"""
users > helpers > teacher_based_helpers > v2_subject_performance_helper.py

This helper provides a unified interface to retrieve subject lists
based on the teacher's role. It ensures that the subject filtering logic
is reusable and role-aware, using proper linking models from the enrollments app.
"""

from the_school.models import Subject
from exams.models import Exam  # ✅ required for HOD logic
from users.models import Teacher
from enrollments.models import (
    TeacherSubjectAssignment,
    ClassGroupTeacherAssignment,
    ClassGroupSubjectAssignment
)


def get_subjects_for_teacher(teacher: Teacher):
    """
    Return a queryset of subjects accessible to the given teacher,
    based on their teacher_role and related enrollments.

    Parameters:
    - teacher (Teacher): The teacher instance whose role will guide subject access.

    Returns:
    - QuerySet[Subject]: List of relevant subjects
    """
    role = teacher.teacher_role

    if role == "Classroom Teacher":
        # Get the class groups the teacher is assigned to
        classgroup_ids = ClassGroupTeacherAssignment.objects.filter(
            teacher=teacher
        ).values_list("class_group_id", flat=True)

        # Subjects assigned to those class groups
        return Subject.objects.filter(
            id__in=ClassGroupSubjectAssignment.objects.filter(
                class_group_id__in=classgroup_ids
            ).values_list("subject_id", flat=True)
        )

    elif role == "Subject Teacher":
        # Subjects assigned to this teacher directly
        return Subject.objects.filter(
            id__in=TeacherSubjectAssignment.objects.filter(
                teacher=teacher
            ).values_list("subject_id", flat=True)
        )

    elif role == "HOD":
        return Subject.objects.filter(department__head_of_department=teacher)

    elif role in ["Principal", "Vice Principal"]:
        # Principals and VPs see all subjects
        return Subject.objects.all()

    # Fallback: no access
    return Subject.objects.none()
