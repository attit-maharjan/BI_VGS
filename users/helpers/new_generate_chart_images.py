# users/helpers/new_generate_chart_images.py

"""
================================================================================
📊 NEW CHART IMAGE HELPER
================================================================================

Purpose:
    Replaces legacy `generate_chart_images.py` with a cleaner, safer, and 
    more modular helper for generating report chart metadata.

- Accepts consistent report card structure
- No reliance on legacy format
- Graceful error handling

Author: Philip Tambiti Leo Walekhwa + Acharya Puskar Raj + Maharjan Attit
================================================================================
"""

def generate_clean_grade_distribution_data(report_card):
    """
    Prepares data for chart rendering based on grade distributions.

    Args:
        report_card (list): List of dictionaries containing:
            - exam_title
            - student_grade
            - grade_distribution

    Returns:
        list: A chart data list ready for rendering.
    """
    chart_data = []
    for entry in report_card:
        distribution = entry.get("grade_distribution", {})
        sorted_grades = sorted(distribution.items())
        chart_data.append({
            "exam_title": entry.get("exam_title"),
            "grade": entry.get("student_grade"),  # Renamed for compatibility
            "labels": [g for g, _ in sorted_grades],
            "values": [c for _, c in sorted_grades],
        })
    return chart_data
