# =============================================================================
# 💬 INTELLIGENT COMMENT GENERATOR (v2)
# Author: Philip Tambiti Leo Walekhwa + Acharya Puskar Raj + Maharjan Attit
# -----------------------------------------------------------------------------
# Description:
# Generates feedback based on student score, grade, and peer comparison within
# the same grade band. The logic varies smartly per grade category.
#
# Input:
# - subject (str): Subject name
# - exam_title (str): Title of the exam
# - grade (str): Letter grade (A-F)
# - score (float): Student’s actual score
# - class_scores_same_grade (List[float]): Peers' scores who got same grade
#
# Output:
# - str: A smart, tailored, motivational comment 🧠📘✨
# =============================================================================

def generate_intelligent_comment(subject, exam_title, grade, score, class_scores_same_grade):
    if not grade or score is None:
        return "No grade or score available to generate feedback."

    avg_grade_score = sum(class_scores_same_grade) / len(class_scores_same_grade) if class_scores_same_grade else 0
    delta = score - avg_grade_score
    comment = f"You scored {round(score, 1)} in {subject}, which falls under grade {grade}. "

    band = grade[0]

    if band == "A":
        comment += f"This is the highest grade band. The average in this group is {avg_grade_score:.1f}. "
        if delta > 2:
            comment += "You're outperforming your peers — excellent work! 🏆"
        elif delta < -2:
            comment += "You're slightly below average for an A — you can dominate with a little push! 🔥"
        else:
            comment += "You're right around the average — still a top performer! ✨"

    elif band == "B":
        comment += f"The average among B-grade students is {avg_grade_score:.1f}. "
        if delta > 2:
            comment += "You're above your group — aim for an A next time! 🚀"
        elif delta < -2:
            comment += "You're slightly below your peers — keep pushing, an A is within reach!"
        else:
            comment += "You're on par with your group — solid performance. 📘"

    elif band == "C":
        comment += f"Your group's average is {avg_grade_score:.1f}. "
        if delta > 2:
            comment += "You're near the top of your group — aim for a B! ✊"
        elif delta < -2:
            comment += "You're trailing behind — review your weak areas and seek support. 📘"
        else:
            comment += "You're right in the middle — solid, but improvement is encouraged. 📈"

    elif band == "D":
        comment += f"This grade band averages {avg_grade_score:.1f}. "
        if delta > 2:
            comment += "You're outperforming others in this band — a climb to C is possible! ⛰️"
        elif delta < -2:
            comment += "You're among the lowest performers here — act fast to avoid slipping further. 🚨"
        else:
            comment += "You're in the middle of a struggling group — time to level up! 🔧"

    elif band == "E":
        comment += "This is a very low grade band. Immediate support and revision is needed. 🙏"

    elif band == "F":
        comment += "You received a failing grade. Seek teacher guidance and commit to a study plan. 📚"

    else:
        comment += "Grade not recognized — please consult your teacher."

    return comment
