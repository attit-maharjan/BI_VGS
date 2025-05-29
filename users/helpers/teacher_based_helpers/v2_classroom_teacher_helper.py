# v2_classroom_teacher_helper.py

from enrollments.models import ClassGroupTeacherAssignment, ClassGroupStudentEnrollment
from users.models import Teacher

def get_assigned_classgroup(teacher_user):
    try:
        teacher = Teacher.objects.get(user=teacher_user)
        return (
            ClassGroupTeacherAssignment.objects
            .filter(teacher=teacher, is_active=True)
            .select_related('class_group')
            .first()
        )
    except Teacher.DoesNotExist:
        return None


def get_students_in_classgroup(class_group):
    if not class_group:
        return []
    return (
        ClassGroupStudentEnrollment.objects
        .filter(class_group=class_group, is_active=True)
        .select_related('student__user')
    )
