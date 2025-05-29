# users/services/teacher_based_services/v2_classroom_teacher_service.py

from users.helpers.teacher_based_helpers.v2_classroom_teacher_helper import (
    get_assigned_classgroup, get_students_in_classgroup
)
from exams.models import StudentMark
from django.db.models import Avg

def get_status_label(score):
    if score is None:
        return "Not Evaluated Yet"
    elif score >= 90:
        return "Excellent"
    elif score >= 80:
        return "Strong Performer"
    elif score >= 70:
        return "Fair"
    elif score >= 60:
        return "Needs Support"
    elif score >= 50:
        return "Struggling"
    else:
        return "At Risk"

def fetch_classgroup_and_students_for_teacher(user):
    """
    Returns class group and students with attached average scores and status labels.
    Only includes data from the class group's academic year.
    """
    classgroup_assignment = get_assigned_classgroup(user)
    if not classgroup_assignment:
        return {"class_group": None, "students": []}

    class_group = classgroup_assignment.class_group
    academic_year = class_group.academic_year
    enrollments = get_students_in_classgroup(class_group)

    # Get all relevant student marks for this class group and academic year
    student_ids = [e.student.id for e in enrollments]
    marks = (
        StudentMark.objects
        .filter(
            student_id__in=student_ids,
            exam__class_group=class_group,
            exam__academic_year=academic_year
        )
        .values('student_id')
        .annotate(avg_score=Avg('score'))
    )

    # Build a map of student_id -> avg_score
    score_map = {
        item['student_id']: round(item['avg_score'], 1) if item['avg_score'] is not None else None
        for item in marks
    }

    # Attach scores and labels to each student instance
    for enrollment in enrollments:
        student = enrollment.student
        avg = score_map.get(student.id)
        student.avg_score = avg
        student.status_label = get_status_label(avg)

    return {
        "class_group": class_group,
        "students": enrollments
    }
