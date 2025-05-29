# ==============================================================================
# 📘 v2_student_exam_insights_context.py
# ==============================================================================
# Role-Agnostic Exam Insight Builders
#
# Modular context services for use across:
# - Parent Dashboards
# - Student Dashboards
# - Teacher Dashboards (Classroom, Subject, HOD)
#
# Includes:
#   - Report Card Charts
#   - Exam Results Summaries
#   - Performance vs Class Avg
#   - Grade Distributions
#   - Subject Comments
#
# 📦 Powered by:
#   ✅ ExamContextAnalyticsService
#   ✅ Grade Distribution Chart Helpers
#   ✅ Score-to-Grade Mapping Helpers
#
# Author: Philip Tambiti Leo Walekhwa + Acharya Puskar Raj + Maharjan Attit
# ==============================================================================




from exams.models import StudentMark
from the_school.models import AcademicYear
from users.services.analytics.new_exam_analytics_service import ExamContextAnalyticsService
from users.services.context.v2_student_metadata_context import (
    get_classgroup_for_student,
    get_class_teacher_for_student,
    get_subjects_for_student
)
from users.helpers.new_generate_chart_images import generate_clean_grade_distribution_data
from users.helpers.v2_generate_subject_comments import generate_subject_comments
from exams.helpers.grade_calculation import get_overall_grade_from_points

from django.db.models import Avg
from django.utils.safestring import mark_safe
import json


# ------------------------------------------------------------------------------
# 🔁 Internal Utility: Enriched student marks
# ------------------------------------------------------------------------------
def _get_enriched_marks(student):
    active_year = AcademicYear.objects.get(is_current=True)
    marks = StudentMark.objects.select_related(
        'exam', 'exam__subject', 'exam__class_group', 'exam__exam_type', 'exam__academic_year'
    ).filter(student=student, exam__academic_year=active_year)

    enriched = []
    for mark in marks:
        exam = mark.exam
        class_avg = StudentMark.objects.filter(exam=exam).aggregate(avg=Avg("score"))['avg'] or 0
        class_grades = list(StudentMark.objects.filter(exam=exam).values_list("grade", flat=True))

        enriched.append({
            "score": float(mark.score),
            "grade": mark.grade,
            "exam": {
                "title": exam.title,
                "exam_code": exam.exam_code,
                "subject": exam.subject.name,
                "exam_type": exam.exam_type.name,
                "date_conducted": exam.date_conducted,
                "max_marks": exam.max_marks,
                "class_group": exam.class_group.name,
                "academic_year": exam.academic_year.name,
                "class_avg": round(class_avg, 2),
                "class_grades": class_grades,
                "points": getattr(exam.grading_scale.grade_ranges.filter(letter=mark.grade).first(), "points", None),
                "grading_scale": exam.grading_scale,
            }
        })

    return enriched


# -------------------------------------------------------------------------
# 📄 V2: Report Card Context (Parent/Global View)
# -------------------------------------------------------------------------
def get_report_card_context(student):
    enriched = _get_enriched_marks(student)
    service = ExamContextAnalyticsService(student, enriched)
    report_card = service.get_grade_insights()
    chart_data = generate_clean_grade_distribution_data(report_card)

    class_group = get_classgroup_for_student(student)
    class_teacher = get_class_teacher_for_student(student)
    subjects = get_subjects_for_student(student)
    subject_count = len(subjects)

    gpa = service.calculate_gpa()
    if gpa is None:
        status_badge_label = "N/A"
        status_badge_class = "bg-gray-200 text-gray-700"
    elif gpa >= 3.7:
        status_badge_label = "Excellent"
        status_badge_class = "bg-green-100 text-green-800"
    elif gpa >= 3.0:
        status_badge_label = "Good"
        status_badge_class = "bg-lime-100 text-lime-800"
    elif gpa >= 2.0:
        status_badge_label = "Average"
        status_badge_class = "bg-yellow-100 text-yellow-800"
    elif gpa >= 1.0:
        status_badge_label = "Needs Help"
        status_badge_class = "bg-orange-100 text-orange-800"
    else:
        status_badge_label = "Critical"
        status_badge_class = "bg-red-100 text-red-800"

    comments = generate_subject_comments(student, enriched)
    snippet_comment = comments[0]["comment"] if comments else "Keep going! You're doing great!"

    subject_scores = {}
    class_averages = {}
    subject_key = {}

    for entry in enriched:
        subject = entry["exam"]["exam_code"]
        label = entry["exam"]["subject"]
        score = entry["score"]
        avg = entry["exam"]["class_avg"]

        subject_scores.setdefault(subject, []).append(score)
        class_averages.setdefault(subject, []).append(avg)
        subject_key[subject] = label

    subject_score_chart = {
        "subjects": list(subject_scores.keys()),
        "student_scores": [sum(scores)/len(scores) for scores in subject_scores.values()],
        "class_averages": [sum(avgs)/len(avgs) for avgs in class_averages.values()]
    }

    exam_codes = [entry["exam"]["exam_code"] for entry in enriched]
    student_scores = [entry["score"] for entry in enriched]
    class_scores = [entry["exam"]["class_avg"] for entry in enriched]

    exam_comparison_chart = {
        "exam_codes": exam_codes,
        "student_scores": [float(s) for s in student_scores],
        "class_averages": [float(c) for c in class_scores]
    }

    overall_grade_data = get_overall_grade_from_points(
        StudentMark.objects.filter(student=student, exam__academic_year__is_current=True)
    )

    return {
        "report_card": report_card,
        "report_charts": chart_data,
        "overall": overall_grade_data,
        "average_grade": overall_grade_data.get("grade", "N/A"),
        "academic_year": class_group.academic_year.name if class_group else "N/A",
        "class_group": class_group.name if class_group else "N/A",
        "class_teacher_name": class_teacher.user.get_full_name() if class_teacher else "N/A",
        "average_score": service.calculate_average_score(),
        "gpa": gpa,
        "status_badge_label": status_badge_label,
        "status_badge_class": status_badge_class,
        "snippet_comment": snippet_comment,
        "subject_score_chart": subject_score_chart,
        "subject_key": subject_key,
        "subject_count": subject_count,
        "exam_comparison_chart": exam_comparison_chart,
    }



# ------------------------------------------------------------------------------
# 📊 Exam Results Summary Context
# ------------------------------------------------------------------------------
def get_exam_results_context(student):
    enriched = _get_enriched_marks(student)

    summary = [
        {
            "subject": entry["exam"]["subject"],
            "exam_code": entry["exam"]["exam_code"],
            "score": entry["score"],
            "grade": entry["grade"],
        }
        for entry in enriched
    ]

    return {
        "summary": summary
    }



# ------------------------------------------------------------------------------
# 📈 Performance Chart Context
# ------------------------------------------------------------------------------
def get_performance_context(student):
    enriched = _get_enriched_marks(student)
    service = ExamContextAnalyticsService(student, enriched)

    chart_data = service.get_performance_chart_data()
    labels = [entry["exam"]["exam_code"] for entry in enriched]
    code_title_map = {entry["exam"]["exam_code"]: entry["exam"]["title"] for entry in enriched}

    return {
        "labels": mark_safe(json.dumps(labels)),
        "student_scores": mark_safe(json.dumps(chart_data["line_chart_data"]["student_scores"], default=float)),
        "class_avg_scores": mark_safe(json.dumps(chart_data["line_chart_data"]["class_avg_scores"], default=float)),
        "code_title_map": code_title_map,
        "exam_code_map_js": mark_safe(json.dumps(code_title_map)),
        "academic_year": enriched[0]["exam"]["academic_year"] if enriched else "N/A",
        "class_group": enriched[0]["exam"]["class_group"] if enriched else "N/A"
    }


# ------------------------------------------------------------------------------
# 📊 Grade Insights Chart Context
# ------------------------------------------------------------------------------
def get_grade_insights_context(student):
    enriched = _get_enriched_marks(student)
    service = ExamContextAnalyticsService(student, enriched)

    insights = service.get_grade_insights()
    chart_data = generate_clean_grade_distribution_data(insights)

    return {
        "insight_charts": mark_safe(json.dumps(chart_data, default=float)),
        "raw_data": chart_data,
        "academic_year": enriched[0]["exam"]["academic_year"] if enriched else "N/A",
        "class_group": enriched[0]["exam"]["class_group"] if enriched else "N/A"
    }


# ------------------------------------------------------------------------------
# 💬 Subject Comments Context
# ------------------------------------------------------------------------------
def get_comments_context(student):
    enriched = _get_enriched_marks(student)
    return {
        "comments": generate_subject_comments(student, enriched)
    }


# ==============================================================================
# 🔁 COMBINED INSIGHTS CONTEXT
# ==============================================================================

def build_exam_insights_for_student(student):
    """
    Combines all core insights into one context object for a student:
    - Subject Scores and Grades
    - Performance Chart (Student vs Class Average)
    - Grade Distribution Chart

    Used by:
    - Classroom Teacher Dashboard
    - Subject Teacher Summary View
    - Parent Insight Panels
    """
    context = get_exam_results_context(student)
    context.update(get_performance_context(student))
    context.update(get_grade_insights_context(student))
    return context

