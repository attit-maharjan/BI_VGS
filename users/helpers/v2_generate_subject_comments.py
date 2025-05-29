# users/helpers/v2_generate_subject_comments.py

"""
===============================================================================
💬 V2 SUBJECT COMMENT GENERATOR (Dict-based for enriched marks)
Compatible with `exam_context_service.py` enriched format.

- Uses the intelligent feedback logic from v2_comment_generation.py.
- Safely handles type errors and data inconsistencies.

Author: Philip Tambiti Leo Walekhwa + Acharya Puskar Raj + Maharjan Attit
===============================================================================
"""

from users.helpers.v2_comment_generation import generate_intelligent_comment

def generate_subject_comments(student, enriched_marks):
    """
    Generates intelligent subject-based comments using enriched mark dicts.

    Args:
        student (Student): The student object
        enriched_marks (List[dict]): List of enriched mark dicts

    Returns:
        List[dict]: List of comments for each subject exam
    """
    comments = []

    for mark in enriched_marks:
        grade = mark.get("grade")
        score = mark.get("score")
        exam = mark.get("exam", {})

        if not grade or score is None:
            continue

        # 🛡️ Defensive: Convert all class scores to float
        raw_class_scores = exam.get("class_grades", [])
        safe_class_scores = []
        for val in raw_class_scores:
            try:
                safe_class_scores.append(float(val))
            except (TypeError, ValueError):
                continue

        comment = generate_intelligent_comment(
            subject=exam.get("subject", "Unknown"),
            exam_title=exam.get("title", "Unknown Exam"),
            grade=grade,
            score=float(score),
            class_scores_same_grade=safe_class_scores
        )

        comments.append({
            "subject": exam.get("subject", "N/A"),
            "exam_title": exam.get("title", "N/A"),
            "grade": grade,
            "comment": comment
        })

    return comments
