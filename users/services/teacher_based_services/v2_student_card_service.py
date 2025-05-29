# users/services/teacher_based_services/v2_student_card_service.py

# ============================
# Imports
# ============================
from users.models import Teacher, Student
from enrollments.models import (
    ClassGroupTeacherAssignment,
    TeacherSubjectAssignment,
    TeacherDepartmentEnrollment,
    ClassGroupStudentEnrollment,
)
from the_school.models import Subject, AcademicYear
from users.helpers.teacher_based_helpers.v2_student_card_helpers import (
    get_status_label,
    get_student_average_score,
    get_class_average_score,
    get_students_by_ids,
    get_all_status_labels,  # ✅ NEW
)
from exams.models import StudentMark
from django.db.models import Avg
from django.core.exceptions import ObjectDoesNotExist

# ============================
# Entry Point: Role-Based Student Fetching
# ============================
def get_students_for_teacher(teacher_user):
    try:
        teacher = Teacher.objects.get(user=teacher_user)
    except ObjectDoesNotExist:
        return []

    role = teacher.teacher_role

    if role == "Classroom Teacher":
        return _get_classroom_students(teacher)
    elif role == "Subject Teacher":
        return _get_subject_students(teacher)
    elif role == "HOD":
        return _get_department_students(teacher)
    elif role in ["Principal", "Vice Principal"]:
        return _get_all_students()
    else:
        return []

# ============================
# Shared Utility: Annotate Student Scores and Status
# ============================
def _annotate_scores(students, academic_year):
    if academic_year is None:
        academic_year = AcademicYear.objects.filter(is_active=True).first()

    if not academic_year:
        return students

    student_ids = [s.id for s in students]
    marks = (
        StudentMark.objects
        .filter(student_id__in=student_ids, exam__academic_year=academic_year)
        .values('student_id')
        .annotate(avg_score=Avg('score'))
    )
    score_map = {
        m['student_id']: round(m['avg_score'], 1) if m['avg_score'] is not None else None
        for m in marks
    }
    for student in students:
        student.avg_score = score_map.get(student.id)
        student.status_label = get_status_label(student.avg_score)
    return students

# ============================
# Role: Classroom Teacher
# ============================
def _get_classroom_students(teacher):
    assignment = (
        ClassGroupTeacherAssignment.objects
        .filter(teacher=teacher, is_active=True)
        .select_related('class_group')
        .first()
    )
    if not assignment:
        return []

    class_group = assignment.class_group
    academic_year = class_group.academic_year

    enrollments = (
        ClassGroupStudentEnrollment.objects
        .filter(class_group=class_group, is_active=True)
        .select_related('student__user')
    )

    students = []
    for enrollment in enrollments:
        student = enrollment.student
        student.class_group = enrollment.class_group  # ✅ Attach manually
        students.append(student)

    return _annotate_scores(students, academic_year)

# ============================
# Role: Subject Teacher
# ============================
def _get_subject_students(teacher):
    subject_assignments = TeacherSubjectAssignment.objects.filter(teacher=teacher, is_active=True)
    subjects = [a.subject for a in subject_assignments]
    years = [a.academic_year for a in subject_assignments]
    student_ids = StudentMark.objects.filter(
        exam__subject__in=subjects,
        exam__academic_year__in=years
    ).values_list('student_id', flat=True).distinct()
    students = get_students_by_ids(student_ids)
    return _annotate_scores(list(students), years[0] if years else None)

# ============================
# Role: Head of Department
# ============================
def _get_department_students(teacher):
    subjects = Subject.objects.filter(department__head_of_department=teacher)
    student_ids = StudentMark.objects.filter(
        exam__subject__in=subjects
    ).values_list('student_id', flat=True).distinct()
    students = get_students_by_ids(student_ids)
    return _annotate_scores(list(students), None)

# ============================
# Role: Principal / Vice Principal
# ============================
def _get_all_students():
    students = get_students_by_ids(Student.objects.values_list('id', flat=True))
    return _annotate_scores(list(students), None)

# ============================
# ✅ NEW: Context Builder for Student Card with Filtering Support
# ============================
def get_student_card_context_for_teacher(request):
    students = get_students_for_teacher(request.user)

    # ✅ Apply status filter from dropdown
    selected_status = request.GET.get("status")
    if selected_status:
        students = [s for s in students if s.status_label == selected_status]

    return {
        "students": students,
        "status_choices": get_all_status_labels(),  # for dropdown
        "selected_status": selected_status,         # to keep filter selection
    }
