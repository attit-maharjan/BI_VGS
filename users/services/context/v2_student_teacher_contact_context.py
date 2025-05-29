### ✅ CONTEXT: users/services/context/v2_student_teacher_contact_context.py
from the_school.models import SchoolSettings, Department
from users.models import Teacher, Student
from enrollments.models import ClassGroupTeacherAssignment, TeacherSubjectAssignment
from users.services.context.v2_student_metadata_context import get_classgroup_for_student, get_subjects_for_student
from django.db.models import Q

def build_student_teacher_contact_context(student):
    classgroup = get_classgroup_for_student(student)
    subjects = get_subjects_for_student(student)
    school = SchoolSettings.objects.first()

    classroom_teacher = ClassGroupTeacherAssignment.objects.filter(
        class_group=classgroup
    ).select_related("teacher__user").first()

    # ✅ Get departments related to subjects
    departments = Department.objects.filter(id__in=subjects.values_list("department_id", flat=True)).distinct()

    # ✅ Extract HODs with their department names
    hods = [
        {
            "teacher": dept.head_of_department,
            "department": dept.name,
            "name": dept.head_of_department.user.get_full_name() if dept.head_of_department else "",
            "email": dept.head_of_department.user.email if dept.head_of_department else ""
        }
        for dept in departments if dept.head_of_department
    ]

    # ✅ Get subject teachers via TeacherSubjectAssignment and attach subjects
    teacher_subject_map = {}
    for tsa in TeacherSubjectAssignment.objects.filter(subject__in=subjects).select_related("teacher", "subject", "teacher__user"):
        tid = tsa.teacher.id
        if tid not in teacher_subject_map:
            teacher_subject_map[tid] = {
                "name": tsa.teacher.user.get_full_name(),
                "email": tsa.teacher.user.email,
                "subjects": []
            }
        teacher_subject_map[tid]["subjects"].append(tsa.subject.name)

    subject_teachers = list(teacher_subject_map.values())

    # ✅ Get principal and vice principal using direct CharField filter
    principal = Teacher.objects.filter(teacher_role__icontains="principal").select_related("user").first()
    vice_principal = Teacher.objects.filter(teacher_role__icontains="vice").select_related("user").first()

    return {
        "student": student,
        "classgroup": classgroup,
        "school_email": school.email_address,
        "school_phone": school.contact_number,
        "principal_name": principal.user.get_full_name() if principal else None,
        "principal_email": principal.user.email if principal else None,
        "vice_principal_name": vice_principal.user.get_full_name() if vice_principal else None,
        "vice_principal_email": vice_principal.user.email if vice_principal else None,
        "classroom_teacher": classroom_teacher.teacher if classroom_teacher else None,
        "hods": hods,
        "subject_teachers": subject_teachers,
    }
