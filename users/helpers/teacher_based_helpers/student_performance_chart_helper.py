"""
Helper: student_performance_chart_helper.py
Location: users/helpers/teacher_based_helpers/

Purpose:
    Aggregates student gender and performance statistics into chart-ready data.
    Supports role-based rendering of bar charts across teacher subroles.
"""

from collections import defaultdict
from users.helpers.teacher_based_helpers.v2_student_card_helpers import get_status_label


def get_chart_data_for_students(students):
    """
    Accepts a list or queryset of Student instances.
    Expects each student to have `.avg_score` and `.user.gender` attributes.

    Returns:
        dict: {
            "Total Students": int,
            "Male": int,
            "Female": int,
            "Outstanding": int,
            "Very Good": int,
            "Good": int,
            "Fair": int,
            "At Risk": int,
            "Critical": int
        }
    """
    chart_data = defaultdict(int)

    categories = [
        "Total Students", "Male", "Female",
        "Outstanding", "Very Good", "Good",
        "Fair", "At Risk", "Critical"
    ]
    for cat in categories:
        chart_data[cat] = 0

    for student in students:
        chart_data["Total Students"] += 1

        # ✅ Access gender via related User model
        gender = (getattr(student.user, "gender", "") or "").strip().lower()
        if gender == "male":
            chart_data["Male"] += 1
        elif gender == "female":
            chart_data["Female"] += 1

        # ✅ Score-based performance band
        avg_score = getattr(student, "avg_score", None)
        label = get_status_label(avg_score)
        if label in categories:
            chart_data[label] += 1

    return dict(chart_data)
