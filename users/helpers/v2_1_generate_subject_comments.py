### ✅ FILE: users/helpers/v2_1_generate_subject_comments.py
import random


def generate_subject_comment(score, class_avg, grade_letter):
    try:
        score = round(float(score), 2)
        class_avg = round(float(class_avg), 2)
        diff = round(score - class_avg, 1)
        proximity_to_next = round(10 - (score % 10), 2) if score < 100 else 0.00

        # ✅ TONE DECISION BASED ON PERFORMANCE
        if score >= 90:
            tone = "celebratory"
        elif diff > 10:
            tone = "encouraging"
        elif -3 <= diff <= 3:
            tone = "supportive"
        elif diff < -10 and score < 60:
            tone = "warning"
        elif class_avg < 55 and 50 <= score <= 70:
            tone = "supportive"
        elif score < 50:
            tone = "warning"
        else:
            tone = "direct"

        # ✅ OPENING PHRASES PER TONE (now complete statements)
        tone_openers = {
            "encouraging": [
                "You're making strong progress.",
                "Good effort — you're heading in the right direction.",
                "There's clear improvement in your performance."
            ],
            "direct": [
                f"You scored {score:.2f} in this exam.",
                f"Your performance was recorded at {score:.2f}.",
                f"Your result: {score:.2f}."
            ],
            "motivating": [
                "Keep pushing your limits.",
                "You're capable of achieving even more.",
                "The journey is ongoing — stay focused."
            ],
            "supportive": [
                "You're not alone — many students found this challenging.",
                "This subject appears demanding across the board.",
                "Keep trying — progress comes step by step."
            ],
            "warning": [
                "This score calls for focused improvement.",
                "Immediate attention is needed in this subject.",
                "Your performance suggests that extra support may be helpful."
            ],
            "celebratory": [
                "Excellent achievement — you're leading the class!",
                "Outstanding work — this is top-tier performance.",
                "Superb result! You've set the bar high."
            ]
        }

        opening = random.choice(tone_openers[tone])

        # ✅ PERFORMANCE CONTEXT
        if class_avg < 55:
            context = f"The class average was {class_avg:.2f}, indicating that many students found this exam difficult."
        else:
            if diff > 10:
                context = f"You outperformed the class by {abs(diff):.1f} points."
            elif 3 <= diff <= 10:
                context = f"You were above the class average of {class_avg:.2f}."
            elif -3 < diff < 3:
                context = f"Your score of {score:.2f} was close to the class average ({class_avg:.2f})."
            elif -10 <= diff <= -3:
                context = f"You were {abs(diff):.1f} points below the class average of {class_avg:.2f}."
            else:
                context = f"You were significantly below the class average by {abs(diff):.1f} points."

        # ✅ GRADE BOOST HINT
        grade_hint = ""
        if 48 <= score <= 89 and proximity_to_next <= 2:
            grade_hint = f" You're just {proximity_to_next:.2f} mark(s) from the next grade."
        elif score < 50:
            grade_hint = " With effort, you can move out of the failing range."

        # ✅ MOTIVATIONAL CLOSERS
        closers = [
            "Keep going.",
            "Progress is possible.",
            "You're improving step by step.",
            "Let’s aim higher next time.",
            "Believe in your growth."
        ]

        # ✅ BUILD FINAL COMMENT
        return f"{opening} {context}{grade_hint} {random.choice(closers)}"

    except Exception:
        return "Score unavailable. Unable to generate a comment at this time."
