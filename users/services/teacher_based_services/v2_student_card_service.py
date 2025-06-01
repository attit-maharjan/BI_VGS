# ============================
# Imports
# ============================
from django.db.models import Avg, Q
from django.core.exceptions import ObjectDoesNotExist

from users.models import Teacher, Student
from enrollments.models import (
    ClassGroupTeacherAssignment,
    TeacherSubjectAssignment,
    TeacherDepartmentEnrollment,
    ClassGroupStudentEnrollment,
)
from the_school.models import Subject, AcademicYear, ClassGroup
from exams.models import StudentMark

from users.helpers.teacher_based_helpers.v2_student_card_helpers import (
    get_status_label,
    get_student_average_score,
    get_class_average_score,
    get_students_by_ids,
    get_all_status_labels,
)

# ============================
# Role-Based Student Fetching
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
    return []

# ============================
# Annotate Student Scores and Status
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
        student.class_group = enrollment.class_group  # attach manually
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
# Student Card Context with Filters
# ============================
def get_student_card_context_for_teacher(request):
    students = get_students_for_teacher(request.user)

    # Fetch filters from request
    selected_status = request.GET.get("status")
    selected_classgroup = request.GET.get("classgroup")
    selected_gender = request.GET.get("gender")

    # Apply filters
    if selected_status:
        students = [s for s in students if s.status_label == selected_status]

    if selected_classgroup:
        students = [
            s for s in students
            if hasattr(s, "class_group") and s.class_group and str(s.class_group.id) == selected_classgroup
        ]

    if selected_gender:
        students = [
            s for s in students
            if s.user.gender and s.user.gender.lower() == selected_gender.lower()
        ]

    # Build filter options
    status_choices = get_all_status_labels()
    classgroup_choices = sorted(
        {s.class_group for s in students if hasattr(s, "class_group") and s.class_group},
        key=lambda cg: cg.name
    )
    gender_choices = sorted(set(
        s.user.gender for s in students if s.user.gender
    ))

    # Determine scope label for heading
    label = None
    if hasattr(request.user, "teacher"):
        teacher = request.user.teacher
        role = teacher.teacher_role

        if role == "Classroom Teacher":
            assignment = teacher.classgroup_assignments.filter(is_active=True).first()
            label = assignment.class_group.name if assignment else "your class group"
        elif role == "HOD":
            departments = teacher.departments_led.filter(is_active=True)
            label = departments.first().name if departments.exists() else "your department"

        elif role in ["Principal", "Vice Principal"]:
            label = "the Entire School"
        elif role == "Subject Teacher":
            assignment = getattr(teacher, "subject_assignment", None)
            subjects = [assignment] if assignment and assignment.is_active else []
            label = subjects[0].subject.name if subjects else "your subject group"


    return {
        "students": students,
        "status_choices": status_choices,
        "classgroup_choices": classgroup_choices,
        "gender_choices": gender_choices,
        "selected_status": selected_status,
        "selected_classgroup": selected_classgroup,
        "selected_gender": selected_gender,
        "student_scope_label": label,
    }
