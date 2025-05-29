# users/templatetags/shared_filters.py

from django import template
from django.urls import reverse
import random

register = template.Library()

# =============================
# 🔎 Utility Filters
# =============================

@register.filter
def dict_get(dictionary, key):
    """Safely get a value from a dictionary in templates"""
    return dictionary.get(key)


# =============================
# 🎨 Score-Based Style Filters
# =============================

@register.filter
def score_to_color(score):
    try:
        score = float(score)
        if score >= 90:
            return "bs-5"
        elif score >= 80:
            return "bs-6"
        elif score >= 70:
            return "bs-9"
        elif score >= 60:
            return "bs-11"
        elif score >= 50:
            return "bs-13"
        else:
            return "bs-14"
    except:
        return "bg-gray-400"

@register.filter
def score_to_border_color_code(score):
    try:
        score = float(score)
        if score >= 90:
            return "#4c9f38"
        elif score >= 80:
            return "#3f7e44"
        elif score >= 70:
            return "#dda63a"
        elif score >= 60:
            return "#fd9d24"
        elif score >= 50:
            return "#ff3a21"
        else:
            return "#e5243b"
    except:
        return "#ccc"

@register.filter
def score_to_text_color(score):
    try:
        score = float(score)
        if score >= 90:
            return "text-bs-5"
        elif score >= 80:
            return "text-bs-6"
        elif score >= 70:
            return "text-bs-9"
        elif score >= 60:
            return "text-bs-11"
        elif score >= 50:
            return "text-bs-13"
        else:
            return "text-bs-14"
    except:
        return "text-gray-400"




@register.filter
def grade_to_color(grade):
    grade = str(grade).upper()
    return {
        "A": "bg-green-600",
        "B": "bg-lime-600",
        "C": "bg-yellow-500",
        "D": "bg-orange-400",
        "E": "bg-pink-500",
        "F": "bg-red-600"
    }.get(grade, "bg-gray-400")




# =============================
# 🔗 Role-Aware Student Dashboard URL
# =============================

@register.simple_tag(takes_context=True)
def student_dashboard_url(context, student):
    """
    Returns a role-aware link to the student dashboard view.
    - For parents: directs to the parent-child dashboard
    - For each teacher subrole: directs to their respective studenthub view
    - Falls back to "#" if no applicable role is matched
    """
    user = context["request"].user

    # 👨‍👩‍👧 Parent Role
    if user.role == "parent":
        return reverse("users:parent_child_dashboard", args=[student.id])

    # 🧑‍🏫 Teacher Role (role-specific branches)
    elif user.role == "teacher" and hasattr(user, "teacher"):
        role = user.teacher.teacher_role

        if role == "Classroom Teacher":
            return reverse("users:classroom_teacher_studenthub", args=[student.id])
        elif role == "Subject Teacher":
            return reverse("users:subject_teacher_studenthub", args=[student.id])
        elif role == "HOD":
            return reverse("users:hod_studenthub", args=[student.id])
        elif role == "Principal":
            return reverse("users:principal_studenthub", args=[student.id])
        elif role == "Vice Principal":
            return reverse("users:vice_principal_studenthub", args=[student.id])

    # 🔁 Default fallback
    return "#"






@register.filter
def random_bs_color(_):
    """
    Returns a random background class from .bs-1 to .bs-17.
    Use it in Django templates to assign random subject card colors.
    """
    return f"bs-{random.randint(1, 17)}"


# =============================
# 🎯 Role-Based Button Class Filter
# =============================

@register.simple_tag(takes_context=True)
def role_button_class(context):
    """
    Returns the appropriate button class name for the current user's role/subrole.
    """
    user = context["request"].user

    if user.role == "student":
        return "bs-student-btn"
    elif user.role == "admin":
        return "bs-admin-btn"
    elif user.role == "parent":
        return "bs-parent-btn"
    elif user.role == "teacher" and hasattr(user, "teacher"):
        role = user.teacher.teacher_role

        if role == "Classroom Teacher":
            return "bs-classroom-teacher-btn"
        elif role == "Subject Teacher":
            return "bs-subject-teacher-btn"
        elif role == "HOD":
            return "bs-hod-btn"
        elif role == "Principal":
            return "bs-principal-btn"
        elif role == "Vice Principal":
            return "bs-vice-principal-btn"

    return "bg-gray-400 text-white"




# =============================
# 🔗 Role-Aware Student URL Tags
# =============================

@register.simple_tag(takes_context=True)
def student_subjects_url(context, student):
    user = context["request"].user
    if user.role == "parent":
        return reverse("users:parent_child_subjects", args=[student.id])
    elif user.role == "teacher" and hasattr(user, "teacher"):
        role = user.teacher.teacher_role
        return {
            "Classroom Teacher": "users:classroom_teacher_student_subjects",
            "Subject Teacher": "users:subject_teacher_student_subjects",
            "HOD": "users:hod_student_subjects",
            "Principal": "users:principal_student_subjects",
            "Vice Principal": "users:vice_principal_student_subjects"
        }.get(role, "#") and reverse({
            "Classroom Teacher": "users:classroom_teacher_student_subjects",
            "Subject Teacher": "users:subject_teacher_student_subjects",
            "HOD": "users:hod_student_subjects",
            "Principal": "users:principal_student_subjects",
            "Vice Principal": "users:vice_principal_student_subjects"
        }[role], args=[student.id])
    return "#"


@register.simple_tag(takes_context=True)
def student_exam_results_url(context, student):
    user = context["request"].user
    if user.role == "parent":
        return reverse("users:parent_child_exam_results", args=[student.id])
    elif user.role == "teacher" and hasattr(user, "teacher"):
        role = user.teacher.teacher_role
        return {
            "Classroom Teacher": "users:classroom_teacher_exam_results",
            "Subject Teacher": "users:subject_teacher_exam_results",
            "HOD": "users:hod_exam_results",
            "Principal": "users:principal_exam_results",
            "Vice Principal": "users:vice_principal_exam_results"
        }.get(role, "#") and reverse({
            "Classroom Teacher": "users:classroom_teacher_exam_results",
            "Subject Teacher": "users:subject_teacher_exam_results",
            "HOD": "users:hod_exam_results",
            "Principal": "users:principal_exam_results",
            "Vice Principal": "users:vice_principal_exam_results"
        }[role], args=[student.id])
    return "#"


@register.simple_tag(takes_context=True)
def student_exam_timetable_url(context, student):
    user = context["request"].user
    if user.role == "parent":
        return reverse("users:parent_child_exam_timetable", args=[student.id])
    elif user.role == "teacher" and hasattr(user, "teacher"):
        role = user.teacher.teacher_role
        return {
            "Classroom Teacher": "users:classroom_teacher_exam_timetable",
            "Subject Teacher": "users:subject_teacher_exam_timetable",
            "HOD": "users:hod_exam_timetable",
            "Principal": "users:principal_exam_timetable",
            "Vice Principal": "users:vice_principal_exam_timetable"
        }.get(role, "#") and reverse({
            "Classroom Teacher": "users:classroom_teacher_exam_timetable",
            "Subject Teacher": "users:subject_teacher_exam_timetable",
            "HOD": "users:hod_exam_timetable",
            "Principal": "users:principal_exam_timetable",
            "Vice Principal": "users:vice_principal_exam_timetable"
        }[role], args=[student.id])
    return "#"


@register.simple_tag(takes_context=True)
def student_grade_insights_url(context, student):
    user = context["request"].user
    if user.role == "parent":
        return reverse("users:parent_child_grade_insights", args=[student.id])
    elif user.role == "teacher" and hasattr(user, "teacher"):
        role = user.teacher.teacher_role
        return {
            "Classroom Teacher": "users:classroom_teacher_grade_insights",
            "Subject Teacher": "users:subject_teacher_grade_insights",
            "HOD": "users:hod_grade_insights",
            "Principal": "users:principal_grade_insights",
            "Vice Principal": "users:vice_principal_grade_insights"
        }.get(role, "#") and reverse({
            "Classroom Teacher": "users:classroom_teacher_grade_insights",
            "Subject Teacher": "users:subject_teacher_grade_insights",
            "HOD": "users:hod_grade_insights",
            "Principal": "users:principal_grade_insights",
            "Vice Principal": "users:vice_principal_grade_insights"
        }[role], args=[student.id])
    return "#"


@register.simple_tag(takes_context=True)
def student_report_card_url(context, student):
    user = context["request"].user
    if user.role == "parent":
        return reverse("users:my_child_report_card", args=[student.id])
    elif user.role == "teacher" and hasattr(user, "teacher"):
        role = user.teacher.teacher_role
        return {
            "Classroom Teacher": "users:classroom_teacher_report_card",
            "Subject Teacher": "users:subject_teacher_report_card",
            "HOD": "users:hod_report_card",
            "Principal": "users:principal_report_card",
            "Vice Principal": "users:vice_principal_report_card"
        }.get(role, "#") and reverse({
            "Classroom Teacher": "users:classroom_teacher_report_card",
            "Subject Teacher": "users:subject_teacher_report_card",
            "HOD": "users:hod_report_card",
            "Principal": "users:principal_report_card",
            "Vice Principal": "users:vice_principal_report_card"
        }[role], args=[student.id])
    return "#"


@register.simple_tag(takes_context=True)
def student_report_card_pdf_url(context, student):
    user = context["request"].user
    if user.role == "parent":
        return reverse("users:parent_printable_report_card", args=[student.id])
    elif user.role == "teacher" and hasattr(user, "teacher"):
        role = user.teacher.teacher_role
        return {
            "Classroom Teacher": "users:classroom_teacher_printable_report_card",
            "Subject Teacher": "users:subject_teacher_printable_report_card",
            "HOD": "users:hod_printable_report_card",
            "Principal": "users:principal_printable_report_card",
            "Vice Principal": "users:vice_principal_printable_report_card"
        }.get(role, "#") and reverse({
            "Classroom Teacher": "users:classroom_teacher_printable_report_card",
            "Subject Teacher": "users:subject_teacher_printable_report_card",
            "HOD": "users:hod_printable_report_card",
            "Principal": "users:principal_printable_report_card",
            "Vice Principal": "users:vice_principal_printable_report_card"
        }[role], args=[student.id])
    return "#"


@register.simple_tag(takes_context=True)
def student_performance_url(context, student):
    user = context["request"].user
    if user.role == "parent":
        return reverse("users:parent_child_performance", args=[student.id])
    elif user.role == "teacher" and hasattr(user, "teacher"):
        role = user.teacher.teacher_role
        return {
            "Classroom Teacher": "users:classroom_teacher_performance",
            "Subject Teacher": "users:subject_teacher_performance",
            "HOD": "users:hod_performance",
            "Principal": "users:principal_performance",
            "Vice Principal": "users:vice_principal_performance"
        }.get(role, "#") and reverse({
            "Classroom Teacher": "users:classroom_teacher_performance",
            "Subject Teacher": "users:subject_teacher_performance",
            "HOD": "users:hod_performance",
            "Principal": "users:principal_performance",
            "Vice Principal": "users:vice_principal_performance"
        }[role], args=[student.id])
    return "#"


@register.simple_tag(takes_context=True)
def student_comments_url(context, student):
    user = context["request"].user
    if user.role == "parent":
        return reverse("users:parent_subject_comments", args=[student.id])
    elif user.role == "teacher" and hasattr(user, "teacher"):
        role = user.teacher.teacher_role
        return {
            "Classroom Teacher": "users:classroom_teacher_subject_comments",
            "Subject Teacher": "users:subject_teacher_subject_comments",
            "HOD": "users:hod_subject_comments",
            "Principal": "users:principal_subject_comments",
            "Vice Principal": "users:vice_principal_subject_comments"
        }.get(role, "#") and reverse({
            "Classroom Teacher": "users:classroom_teacher_subject_comments",
            "Subject Teacher": "users:subject_teacher_subject_comments",
            "HOD": "users:hod_subject_comments",
            "Principal": "users:principal_subject_comments",
            "Vice Principal": "users:vice_principal_subject_comments"
        }[role], args=[student.id])
    return "#"


@register.simple_tag(takes_context=True)
def student_contact_teachers_url(context, student):
    user = context["request"].user
    if user.role == "parent":
        return reverse("users:parent_teacher_contacts", args=[student.id])
    elif user.role == "teacher" and hasattr(user, "teacher"):
        role = user.teacher.teacher_role
        return {
            "Classroom Teacher": "users:classroom_teacher_teacher_contacts",
            "Subject Teacher": "users:subject_teacher_teacher_contacts",
            "HOD": "users:hod_teacher_contacts",
            "Principal": "users:principal_teacher_contacts",
            "Vice Principal": "users:vice_principal_teacher_contacts"
        }.get(role, "#") and reverse({
            "Classroom Teacher": "users:classroom_teacher_teacher_contacts",
            "Subject Teacher": "users:subject_teacher_teacher_contacts",
            "HOD": "users:hod_teacher_contacts",
            "Principal": "users:principal_teacher_contacts",
            "Vice Principal": "users:vice_principal_teacher_contacts"
        }[role], args=[student.id])
    return "#"
