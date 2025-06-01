from django.db.models import Avg, Q
from users.models import Teacher, Student
from enrollments.models import (
    ClassGroupTeacherAssignment,
    TeacherSubjectAssignment,
    TeacherDepartmentEnrollment,
    ClassGroupStudentEnrollment
)
from the_school.models import Subject, AcademicYear, Department, ClassGroup
from exams.models import StudentMark
from users.helpers.teacher_based_helpers.student_performance_chart_helper import get_chart_data_for_students


def get_chart_data_list_for_teacher(request):
    teacher = getattr(request.user, "teacher", None)
    if not teacher:
        return []

    role = teacher.teacher_role
    if role == "Classroom Teacher":
        return _get_classgroup_subject_charts(teacher)
    elif role == "Subject Teacher":
        return _get_subject_teacher_charts(teacher)
    elif role == "HOD":
        return _get_department_subject_charts(teacher)
    elif role in ["Principal"]:
        return _get_all_subject_charts(request)
    elif role in ["Vice Principal"]:
        return _get_all_subject_charts(request)
    return []


def _get_classgroup_subject_charts(teacher):
    data = []
    assignment = (
        ClassGroupTeacherAssignment.objects
        .filter(teacher=teacher, is_active=True)
        .select_related("class_group")
        .first()
    )
    if not assignment:
        return data

    class_group = assignment.class_group
    student_ids = ClassGroupStudentEnrollment.objects.filter(
        class_group=class_group, is_active=True
    ).values_list("student_id", flat=True)

    subject_ids = StudentMark.objects.filter(
        student_id__in=student_ids
    ).values_list("exam__subject_id", flat=True).distinct()

    subjects = Subject.objects.filter(id__in=subject_ids)

    for subject in subjects:
        students = _get_students_for_subject(subject, student_ids)
        raw = get_chart_data_for_students(students)
        data.append({
            "label": f"{subject.name} – {class_group.name}",
            "labels": list(raw.keys()),
            "data": list(raw.values())
        })
    return data


def _get_subject_teacher_charts(teacher):
    data = []
    assignments = TeacherSubjectAssignment.objects.filter(
        teacher=teacher, is_active=True
    ).select_related("subject")

    for assign in assignments:
        subject = assign.subject
        subject_assignments = subject.class_assignments.filter(is_active=True)

        for sa in subject_assignments:
            class_group = sa.class_group
            student_ids = ClassGroupStudentEnrollment.objects.filter(
                class_group=class_group, is_active=True
            ).values_list("student_id", flat=True)

            students = _get_students_for_subject(subject, student_ids)
            if students:
                raw = get_chart_data_for_students(students)
                data.append({
                    "label": f"{subject.name} – {class_group.name}",
                    "labels": list(raw.keys()),
                    "data": list(raw.values())
                })
    return data


def _get_department_subject_charts(teacher):
    data = []

    department_subjects = Subject.objects.filter(
        department__head_of_department=teacher
    ).distinct()

    for subject in department_subjects:
        student_ids = StudentMark.objects.filter(
            exam__subject=subject
        ).values_list("student_id", flat=True).distinct()

        students = _get_students_for_subject(subject, student_ids)
        raw = get_chart_data_for_students(students)
        data.append({
            "label": f"{subject.name}",
            "labels": list(raw.keys()),
            "data": list(raw.values())
        })

    return data


def _get_all_subject_charts(request):
    data = []

    # Retrieve filter values from GET
    academic_year_id = request.GET.get("academic_year")
    department_id = request.GET.get("department")
    class_group_id = request.GET.get("classgroup")

    # Base queryset
    subjects = Subject.objects.all()

    if department_id:
        subjects = subjects.filter(department_id=department_id)

    if academic_year_id:
        subjects = subjects.filter(
            class_assignments__academic_year_id=academic_year_id
        ).distinct()

    for subject in subjects:
        class_assignments = subject.class_assignments.filter(is_active=True)

        if academic_year_id:
            class_assignments = class_assignments.filter(academic_year_id=academic_year_id)

        if class_group_id:
            class_assignments = class_assignments.filter(class_group_id=class_group_id)

        for sa in class_assignments:
            class_group = sa.class_group
            student_ids = ClassGroupStudentEnrollment.objects.filter(
                class_group=class_group, is_active=True
            ).values_list("student_id", flat=True)

            students = _get_students_for_subject(subject, student_ids)
            if students:
                raw = get_chart_data_for_students(students)
                data.append({
                    "label": f"{subject.name} – {class_group.name}",
                    "labels": list(raw.keys()),
                    "data": list(raw.values())
                })

    return data


def _get_students_for_subject(subject, student_ids):
    students = Student.objects.filter(id__in=student_ids).select_related("user")
    for student in students:
        avg = StudentMark.objects.filter(
            student=student, exam__subject=subject
        ).aggregate(score_avg=Avg("score"))["score_avg"]
        student.avg_score = round(avg, 1) if avg is not None else None
    return students
