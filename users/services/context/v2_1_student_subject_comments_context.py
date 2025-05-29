### ✅ FILE: users/services/context/v2_1_student_subject_comments_context.py
from exams.models import StudentMark
from users.models import Student
from enrollments.models import ClassGroupStudentEnrollment
from the_school.models import Subject
from users.helpers.v2_1_generate_subject_comments import generate_subject_comment

from django.db.models import Avg

def build_student_subject_comments_context(student):
    enrollment = ClassGroupStudentEnrollment.objects.select_related("class_group").filter(
        student=student, is_active=True
    ).first()
    classgroup = enrollment.class_group if enrollment else None

    subjects = Subject.objects.filter(grade_level=classgroup.grade_level)
    comments = []

    for subject in subjects:
        mark = StudentMark.objects.filter(student=student, exam__subject=subject).order_by("-exam__date_conducted").first()
        if not mark:
            continue

        class_avg = StudentMark.objects.filter(
            exam=mark.exam,
            student__in=Student.objects.filter(class_group_enrollments__class_group=classgroup)
        ).aggregate(avg=Avg("score"))['avg'] or 0

        comment = generate_subject_comment(mark.score, class_avg, mark.grade)

        comments.append({
            "subject": subject.name,
            "exam": mark.exam.title,
            "score": mark.score,
            "class_avg": round(class_avg, 1),
            "grade": mark.grade,
            "comment": comment
        })

    return {
        "student": student,
        "classgroup": classgroup,
        "subject_comments": comments
    }
