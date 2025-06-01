
from exams.models import StudentMark
from users.models import Student
from django.db.models import Avg

# ✅ NEW: Centralized thresholds and labels
STATUS_LABELS = [
    ("Outstanding", 90),
    ("Very Good", 80),
    ("Good", 70),
    ("Fair", 60),
    ("At Risk", 50),
    ("Critical", 0),
]

# ✅ NEW: For dropdowns and consistent label sets
def get_all_status_labels():
    return [label for label, _ in STATUS_LABELS]

# ✅ REFACTORED: Same logic, but now consistent with STATUS_LABELS
def get_status_label(score):
    if score is None:
        return "Not Evaluated Yet"
    score = float(score)
    for label, threshold in STATUS_LABELS:
        if score >= threshold:
            return label
    return "Critical"  # fallback

# ✅ UNTOUCHED: All original functions
def get_student_average_score(student_id, academic_year=None):
    qs = StudentMark.objects.filter(student_id=student_id)
    if academic_year:
        qs = qs.filter(exam__academic_year=academic_year)
    return qs.aggregate(avg_score=Avg("score"))['avg_score']

def get_class_average_score(class_group):
    from enrollments.models import ClassGroupStudentEnrollment

    student_ids = ClassGroupStudentEnrollment.objects.filter(
        class_group=class_group, is_active=True
    ).values_list("student_id", flat=True)

    return StudentMark.objects.filter(
        student_id__in=student_ids, exam__class_group=class_group
    ).aggregate(avg_score=Avg("score"))['avg_score']

def get_students_by_ids(ids):
    from enrollments.models import ClassGroupStudentEnrollment

    students = Student.objects.filter(id__in=ids).select_related("user")

    enrollment_map = {
        e.student_id: e.class_group
        for e in ClassGroupStudentEnrollment.objects.filter(
            student_id__in=ids,
            is_active=True
        ).select_related("class_group")
    }

    for student in students:
        student.class_group = enrollment_map.get(student.id)

    return students
