from enrollments.models import TeacherSubjectAssignment, ClassGroupSubjectAssignment, ClassGroupStudentEnrollment
from exams.models import StudentMark, Exam

def get_students_for_exam_update(exam_id, teacher):
    try:
        exam = Exam.objects.get(id=exam_id)
    except Exam.DoesNotExist:
        return StudentMark.objects.none()

    # Ensure the teacher is assigned to the subject in this exam
    if not TeacherSubjectAssignment.objects.filter(teacher=teacher, subject=exam.subject).exists():
        return StudentMark.objects.none()

    # Get class groups for this subject
    class_group_ids = ClassGroupSubjectAssignment.objects.filter(
        subject=exam.subject
    ).values_list('class_group_id', flat=True)

    # Get students in those class groups
    student_ids = ClassGroupStudentEnrollment.objects.filter(
        class_group_id__in=class_group_ids
    ).values_list('student_id', flat=True)

    # Return StudentMark queryset (MUST be a QuerySet, not a list)
    return StudentMark.objects.filter(
        exam=exam,
        student_id__in=student_ids
    ).select_related('student')
