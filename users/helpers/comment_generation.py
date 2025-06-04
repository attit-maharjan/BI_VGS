# +++++++++++++++++++++++++++++++++++++++++++++
# 📄 Intelligent Feedback Generator
# Description: Produces subject-wise exam feedback based on peer comparison
# +++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 📄 Intelligent Feedback Generator — Student-Focused Psychological Commentary
#
# Description:
# This module generates subject-specific performance comments intended 
# exclusively for students. The comments are tone-aware, psychologically 
# calibrated, and motivational in nature. They are designed to:
#
# - Encourage self-reflection and personal growth
# - Deliver feedback in a supportive, empowering tone
# - Reduce performance anxiety by contextualizing peer comparison
#
# 🔄 DIFFERENCE FROM TEACHER / PARENT COMMENTS:
# These comments are distinct from those shown to teachers or parents.
# While teacher and parent comments may emphasize diagnostic insight,
# comparative ranking, or academic intervention, these student comments
# prioritize emotional intelligence, intrinsic motivation, and resilience.
#
# The goal is to help students understand their performance while maintaining
# self-confidence and a growth mindset — not to evaluate or critique from
# an external perspective.
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


import random


def generate_intelligent_comment(subject, exam_title, grade, score, class_scores_same_grade):
    """
    Generates a subject-specific, tone-aware comment based on score, grade, and peer performance.
    """

    if not grade or score is None:
        return "No grade or score available to generate feedback."

    # Remove the student's own score from peer list
    peer_scores = [s for s in class_scores_same_grade if s != score]
    avg_grade_score = sum(peer_scores) / len(peer_scores) if peer_scores else score
    delta = round(score - avg_grade_score, 1)
    proximity = round(10 - (score % 10), 2) if score < 100 else 0.00

    # Determine the overall tone of the comment
    if score >= 90:
        tone = "celebratory"
    elif delta > 10:
        tone = "encouraging"
    elif -3 <= delta <= 3:
        tone = "supportive"
    elif delta < -10 and score < 60:
        tone = "warning"
    elif avg_grade_score < 55 and 50 <= score <= 70:
        tone = "supportive"
    elif score < 50:
        tone = "warning"
    else:
        tone = "direct"

    tone_openers = {
        "encouraging": [
            f"You're making strong progress in {subject}.",
            f"Good effort in {subject} — you're heading in the right direction.",
            f"{subject} performance is improving steadily."
        ],
        "direct": [
            f"You scored {score:.1f} in {subject}.",
            f"Your performance in {subject} was recorded at {score:.1f}.",
            f"Your result in {subject}: {score:.1f}."
        ],
        "supportive": [
            f"{subject} appears challenging, but your effort is noted.",
            f"This was a demanding {subject} exam for many.",
            f"Stay consistent in {subject} — improvement follows persistence."
        ],
        "warning": [
            f"This result in {subject} signals the need for focused support.",
            f"{subject} requires more attention moving forward.",
            f"You may benefit from extra help in {subject} to catch up."
        ],
        "celebratory": [
            f"Excellent achievement in {subject} — you're among the top performers!",
            f"Outstanding work in {subject} — this is top-tier performance.",
            f"Superb result in {subject}! You've set a high standard."
        ]
    }

    opening = random.choice(tone_openers[tone])

    # Add context based on class performance comparison
    if peer_scores:
        if avg_grade_score < 55:
            context = f" The class average was {avg_grade_score:.1f}, suggesting this was a tough exam."
        elif delta > 10:
            context = f" You outperformed your peers by {abs(delta):.1f} points."
        elif 3 <= delta <= 10:
            context = f" You scored above the class average of {avg_grade_score:.1f}."
        elif -3 < delta < 3:
            context = f" Your score of {score:.1f} was close to the class average ({avg_grade_score:.1f})."
        elif -10 <= delta <= -3:
            context = f" You were {abs(delta):.1f} points below the class average."
        else:
            context = f" You were significantly below the class average by {abs(delta):.1f} points."
    else:
        if grade in ["F", "E", "D"]:
            context = f" This result in {subject} stands out individually — focus on personal improvement."
        elif grade == "C":
            context = f" Your effort in {subject} is noted even without a peer benchmark."
        else:
            context = f" In {subject}, your performance is strong — though no direct peer comparison was available."

    grade_hint = ""
    if 48 <= score <= 89 and proximity <= 2:
        grade_hint = f" You're just {proximity:.2f} mark(s) from the next grade."
    elif score < 50:
        grade_hint = " With effort, you can move out of the failing range."

    closers = random.sample([
        "Keep going.",
        "Progress is possible.",
        "You're improving step by step.",
        "Let’s aim higher next time.",
        "Believe in your growth.",
        "You're on a good path — keep refining it.",
        "Consistency will raise your performance."
    ], k=3)

    return f"{opening}{context}{grade_hint} {random.choice(closers)}"


def generate_subject_comments(student, marks):
    """
    Generates subject-specific comments based on performance in the student’s exams.
    """

    comments = []
    for mark in marks:
        if not mark.grade:
            continue

        peer_scores = mark.exam.studentmark_set.filter(grade=mark.grade).values_list("score", flat=True)

        comment = generate_intelligent_comment(
            subject=mark.exam.subject.name,
            exam_title=mark.exam.title,
            grade=mark.grade,
            score=mark.score,
            class_scores_same_grade=list(peer_scores)
        )

        comments.append({
            "subject": mark.exam.subject.name,
            "exam_title": mark.exam.title,
            "grade": mark.grade,
            "comment": comment
        })

    return comments
