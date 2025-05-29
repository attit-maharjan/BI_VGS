# users/services/analytics/new_exam_analytics_service.py

"""
================================================================================
🧠 EXAM CONTEXT ANALYTICS SERVICE (ExamContextAnalyticsService)
================================================================================

📍 Purpose:
    Please note that Student was done on the older ExamContextAnalyticsService
    We can change it to use this new one just as Parent and all Teacher

🎯 Key Features:
    - GPA calculation
    - Average score computation
    - Exam summaries
    - Performance trend extraction
    - Grade distribution for charts

🚫 No dependencies on legacy files — uses only enriched marks as input.

Author: Philip Tambiti Leo Walekhwa + Acharya Puskar Raj + Maharjan Attit

================================================================================
"""

from collections import defaultdict, Counter
from statistics import mean

class ExamContextAnalyticsService:
    def __init__(self, student, enriched_marks):
        self.student = student
        self.enriched_marks = enriched_marks

    # ----------------------------------------
    # 🎓 GPA & Grade Info
    # ----------------------------------------
    def calculate_gpa(self):
        points = [
            entry["exam"].get("points")
            for entry in self.enriched_marks
            if entry["exam"].get("points") is not None
        ]
        return round(sum(points) / len(points), 2) if points else None

    # ----------------------------------------
    # 📊 Average Score
    # ----------------------------------------
    def calculate_average_score(self):
        scores = [entry["score"] for entry in self.enriched_marks if "score" in entry]
        return round(mean(scores), 2) if scores else None

    # ----------------------------------------
    # 📄 Exam Summary
    # ----------------------------------------
    def generate_exam_summary(self):
        summary = []
        for entry in self.enriched_marks:
            exam = entry["exam"]
            summary.append({
                "title": exam["title"],
                "code": exam["exam_code"],
                "subject": exam["subject"],
                "type": exam["exam_type"],
                "date": exam["date_conducted"],
                "score": entry["score"],
                "grade": entry["grade"],
                "class_avg": exam["class_avg"],
                "max_marks": exam["max_marks"],
            })
        return summary

    # ----------------------------------------
    # 📈 Performance Line Chart Data
    # ----------------------------------------
    def get_performance_chart_data(self):
        return {
            "line_chart_data": {
                "student_scores": [entry["score"] for entry in self.enriched_marks],
                "class_avg_scores": [entry["exam"]["class_avg"] for entry in self.enriched_marks],
            }
        }

    # ----------------------------------------
    # 📊 Grade Insights (for bar/pie charts)
    # ----------------------------------------
    def get_grade_insights(self):
        insight_data = []
        exam_groups = defaultdict(list)

        for entry in self.enriched_marks:
            exam_title = entry["exam"]["title"]
            exam_groups[exam_title].append(entry["grade"])

        for title, grades in exam_groups.items():
            grade_dist = dict(Counter(grades))
            student_grade = next(
                (e["grade"] for e in self.enriched_marks if e["exam"]["title"] == title), "N/A"
            )
            insight_data.append({
                "exam_title": title,
                "student_grade": student_grade,
                "grade_distribution": grade_dist
            })

        return insight_data
