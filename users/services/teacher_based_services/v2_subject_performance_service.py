"""
users > services > teacher_based_services > v2_subject_performance_service.py

This service calculates analytics for a given set of subjects,
including average scores, grade distribution, pass rate, and more.
It is designed to be reusable across all teacher roles.
"""

from exams.models import StudentMark, Exam
from the_school.models import Subject
from enrollments.models import TeacherSubjectAssignment, ClassGroupSubjectAssignment
from statistics import mean, stdev
from collections import Counter
from django.db.models import Avg, Max, Min


def compute_grade_distribution(marks_queryset):
    """
    Computes the grade distribution for a given queryset of StudentMark entries.
    Returns a dictionary with grade letters as keys and counts as values.
    """
    grades = [mark.grade for mark in marks_queryset if mark.grade]
    return dict(Counter(grades))


def calculate_subject_performance(subjects):
    """
    Generate analytics for a list or queryset of subjects.

    Parameters:
    - subjects (QuerySet[Subject]): The subjects to process.

    Returns:
    - List[Dict]: A list of dictionaries with analytics per subject.
    """
    analytics = []

    for subject in subjects:
        marks = StudentMark.objects.filter(exam__subject=subject)
        scores = list(marks.values_list("score", flat=True))

        if scores:
            avg_score = round(mean(scores), 2)
            std_dev = round(stdev(scores), 2) if len(scores) > 1 else 0.0
            highest = max(scores)
            lowest = min(scores)
            pass_count = sum(score >= 50 for score in scores)
            pass_rate = round((pass_count / len(scores)) * 100, 2)
        else:
            avg_score = std_dev = highest = lowest = pass_rate = 0

        grade_dist = dict(sorted(compute_grade_distribution(marks).items()))

        exam_count = Exam.objects.filter(subject=subject).count()
        last_exam = Exam.objects.filter(subject=subject).order_by("-date_conducted").first()

        # ✅ Enrich with subject teacher and class groups
        subject_teacher = (
            subject.assigned_teachers.first().teacher.user.get_full_name()
            if subject.assigned_teachers.exists()
            else "Unassigned"
        )

                        
        

        class_groups = list(
            ClassGroupSubjectAssignment.objects.filter(subject=subject)
            .values_list("class_group__name", flat=True)
        )

        analytics.append({
            "subject": subject,
            "average_score": avg_score,
            "std_deviation": std_dev,
            "highest_score": highest,
            "lowest_score": lowest,
            "pass_rate": pass_rate,
            "grade_distribution": grade_dist,
            "exam_count": exam_count,
            "last_exam_date": last_exam.date_conducted if last_exam else None,
            "subject_teacher": subject_teacher,
            "class_groups": class_groups,
        })

    return analytics
