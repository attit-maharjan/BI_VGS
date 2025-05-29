"""
================================================================================
📁 STUDENT METADATA CONTEXT SERVICE
================================================================================

Provides reusable functions to retrieve basic, non-analytical information
about a student's academic environment.

Includes:
    - Subjects assigned to student via class group
    - Class group details
    - Classroom teacher (if assigned)
    - Enrollment details

🔁 Used across dashboards (Parent, Teacher, Admin, etc.)

Author: Philip Tambiti Leo Walekhwa + Acharya Puskar Raj + Maharjan Attit
================================================================================
"""

from enrollments.models import (
    TeacherSubjectAssignment,
    ClassGroupStudentEnrollment,
    ClassGroupTeacherAssignment,
)
from the_school.models import Subject, AcademicYear

# ==============================================================================
# 📘 SUBJECTS + TEACHERS FOR STUDENT
# ==============================================================================

def get_subjects_with_teachers_for_student(student):
    """
    Returns a list of subjects the student is taking and their assigned teachers (if any).
    Each item includes subject details and the teacher assigned to that subject.
    """
    try:
        enrollment = ClassGroupStudentEnrollment.objects.select_related('class_group').get(student=student)
        class_group = enrollment.class_group
        academic_year = class_group.academic_year
        subjects = class_group.grade_level.subjects.all()
    except ClassGroupStudentEnrollment.DoesNotExist:
        return []

    result = []

    for subject in subjects:
        teacher_assignment = TeacherSubjectAssignment.objects.filter(
            subject=subject,
            academic_year=academic_year,
            is_active=True
        ).select_related("teacher__user").first()

        result.append({
            "subject": subject,
            "teacher": teacher_assignment.teacher if teacher_assignment else None
        })

    return result

# ==============================================================================
# 🧑‍🎓 GET CLASS GROUP FOR STUDENT
# ==============================================================================

def get_classgroup_for_student(student):
    """
    Returns the student's assigned class group (or None).
    """
    try:
        enrollment = ClassGroupStudentEnrollment.objects.select_related('class_group').get(student=student)
        return enrollment.class_group
    except ClassGroupStudentEnrollment.DoesNotExist:
        return None

# ==============================================================================
# 🧑‍🏫 GET CLASS GROUP FOR CLASSROOM TEACHER
# ==============================================================================

def get_classgroup_for_teacher(teacher):
    """
    Returns the ClassGroup assigned to a Classroom Teacher.

    Only returns if:
    - teacher has an active assignment
    - assumes current year filtering is handled globally
    """
    try:
        assignment = ClassGroupTeacherAssignment.objects.select_related('class_group').get(
            teacher=teacher,
            is_active=True
        )
        return assignment.class_group
    except ClassGroupTeacherAssignment.DoesNotExist:
        return None

# ==============================================================================
# 👩‍🏫 GET CLASS TEACHER FOR A STUDENT
# ==============================================================================

def get_class_teacher_for_student(student):
    """
    Returns the assigned classroom teacher for the student's class group (if any).
    """
    class_group = get_classgroup_for_student(student)
    if not class_group:
        return None

    try:
        assignment = ClassGroupTeacherAssignment.objects.get(
            class_group=class_group,
            teacher__teacher_role='Classroom Teacher',
            is_active=True
        )
        return assignment.teacher
    except ClassGroupTeacherAssignment.DoesNotExist:
        return None

# ==============================================================================
# 📚 GET SUBJECTS FOR STUDENT
# ==============================================================================

def get_subjects_for_student(student):
    """
    Returns all subjects assigned to the student's class group.
    """
    class_group = get_classgroup_for_student(student)
    if not class_group:
        return []
    return class_group.grade_level.subjects.all()

# ==============================================================================
# 🧩 FULL SUBJECT CONTEXT BLOCK
# ==============================================================================

def build_student_subject_metadata_context(student):
    """
    Returns context for rendering subject overview cards including:
    - student model instance
    - student_id
    - classgroup (active)
    - student_subjects with teacher info and profile photo
    """
    try:
        enrollment = ClassGroupStudentEnrollment.objects.select_related('class_group').get(student=student)
        class_group = enrollment.class_group
    except ClassGroupStudentEnrollment.DoesNotExist:
        return {
            "student": student,
            "student_id": student.student_id,
            "classgroup": None,
            "student_subjects": []
        }

    subjects = class_group.grade_level.subjects.all()
    academic_year = class_group.academic_year
    subject_data = []

    for subject in subjects:
        teacher_assignment = TeacherSubjectAssignment.objects.filter(
            subject=subject,
            academic_year=academic_year,
            is_active=True
        ).select_related('teacher__user').first()

        if teacher_assignment and teacher_assignment.teacher:
            teacher = teacher_assignment.teacher
            user = teacher.user
            teacher_name = user.get_full_name()
            teacher_email = user.email
            teacher_profile_image = user.profile_image.url if user.profile_image else None
        else:
            teacher_name = None
            teacher_email = None
            teacher_profile_image = None

        subject_data.append({
            "name": subject.name,
            "code": subject.code,
            "teacher_name": teacher_name,
            "teacher_email": teacher_email,
            "teacher_profile_image": teacher_profile_image,
        })

    return {
        "student": student,
        "student_id": student.student_id,
        "classgroup": class_group,
        "student_subjects": subject_data
    }


# ==============================================================================
# 👥 GET STUDENTS IN A CLASS GROUP
# ==============================================================================

def get_students_in_classgroup(classgroup):
    """
    Returns a list of all students enrolled in a given class group.
    """
    return [
        enrollment.student
        for enrollment in ClassGroupStudentEnrollment.objects.select_related('student').filter(
            class_group=classgroup,
            is_active=True
        )
    ]
