# ✅ File: users/helpers/teacher_based_helpers/subject_teacher_access_control.py

from django.core.exceptions import PermissionDenied
from enrollments.models import TeacherSubjectAssignment


def validate_subject_teacher_access(user, subject):
    """
    Ensures that the teacher is assigned to the given subject.
    If not, raise PermissionDenied.
    """
    if user.role != "teacher" or not hasattr(user, "teacher"):
        raise PermissionDenied("User is not a teacher.")

    teacher = user.teacher

    is_assigned = TeacherSubjectAssignment.objects.filter(
        teacher=teacher,
        subject=subject,
        is_active=True
    ).exists()

    if not is_assigned:
        raise PermissionDenied("Access denied: you are not assigned to this subject.")
