import plotly.graph_objs as go
from collections import Counter
from exams.models import StudentMark, GradeRange
from enrollments.models import ClassGroupStudentEnrollment


def get_letter_grade(score):
    """Returns the letter grade for a given numeric score."""
    grade_range = GradeRange.objects.filter(min_percentage__lte=score, max_percentage__gte=score).first()
    return grade_range.letter if grade_range else 'F'


def generate_grade_distribution_charts(student, exams, class_group):
    charts = []

    default_bar_color = "#0a97d9"        # .bs-2 sea blue
    student_highlight_color = "#111827"  # charcoal

    # 🎨 Grade-color mapping for icon (matches theme)
    grade_colors = {
        "A": "#4c9f38",   # green
        "B": "#26bde2",   # light blue
        "C": "#facc15",   # yellow
        "D": "#fb923c",   # orange
        "E": "#f97316",   # deep orange
        "F": "#dc2626",   # red
    }

    class_student_ids = ClassGroupStudentEnrollment.objects.filter(
        class_group=class_group,
        is_active=True
    ).values_list("student_id", flat=True)

    for exam in exams:
        class_marks = StudentMark.objects.filter(
            exam=exam,
            student_id__in=class_student_ids
        ).select_related("student")

        grades = []
        student_grade = None

        for mark in class_marks:
            grade = get_letter_grade(mark.score or 0)
            grades.append(grade)
            if mark.student_id == student.id:
                student_grade = grade

        grade_counts = Counter(grades)
        all_grades = ['A', 'B', 'C', 'D', 'E', 'F']
        y = [grade_counts.get(g, 0) for g in all_grades]

        colors = [default_bar_color] * len(all_grades)
        if student_grade in all_grades:
            idx = all_grades.index(student_grade)
            colors[idx] = student_highlight_color

        trace = go.Bar(
            x=all_grades,
            y=y,
            marker=dict(color=colors),
            text=y,
            textposition='auto'
        )

        layout = go.Layout(
            title=dict(
                text=exam.title,
                font=dict(size=18, color='#0f172a', family='Roboto, Arial, sans-serif'),
                xanchor='center',
                x=0.5
            ),
            xaxis=dict(
                title=dict(
                    text='Grade',
                    font=dict(size=16, color='#0f172a', family='Roboto')
                ),
                tickfont=dict(size=15, color='#334155', family='Roboto'),
                showgrid=False,
                zeroline=False
            ),
            yaxis=dict(
                title=dict(
                    text='Number of Students',
                    font=dict(size=16, color='#0f172a', family='Roboto, Arial, sans-serif')
                ),
                tickfont=dict(size=15, color='#334155', family='Roboto, Arial, sans-serif'),
                gridcolor='rgba(203,213,225,0.5)'
            ),
            font=dict(size=15, color='#111827', family='Roboto, Arial, sans-serif'),
            plot_bgcolor='#ffffff',
            paper_bgcolor='#f9fafb',
            margin=dict(l=60, r=40, t=80, b=60),
            showlegend=False,
            transition=dict(duration=800, easing="cubic-in-out")
        )

        fig = go.Figure(data=[trace], layout=layout)
        fig.update_traces(marker_line_width=1.5, marker_line_color='white')

        # 🧠 Header with icon + grade + count
        student_grade_count = grade_counts.get(student_grade, 0)
        icon_color = grade_colors.get(student_grade, "#6b7280")

        student_label = (
            f"<h3 style='text-align:center; font-family:Roboto, sans-serif; font-size:18px; margin-bottom:12px;'>"
            f"<i class='fas fa-star' style='color:{icon_color}; margin-right:8px;'></i>"
            f"<span style='color:#0f172a;'>Scored Grade <strong>{student_grade}</strong>, with "
            f"{student_grade_count-1 } other student{'s' if student_grade_count != 1 else ''}</span>"
            f"</h3>"
        )

        charts.append(student_label + fig.to_html(full_html=False))

    return charts




def get_letter_grade(score):
    """Returns the letter grade for a given numeric score."""
    grade_range = GradeRange.objects.filter(min_percentage__lte=score, max_percentage__gte=score).first()
    return grade_range.letter if grade_range else 'F'


def compute_gpa_and_average_grade(marks):
    """
    More realistic GPA + average grade calculator using earned grade letters and
    scale-defined point mappings — adapted from the original exams helper.
    """
    from exams.models import GradeRange

    total_points = 0
    total_exams = 0
    scale = None  # Use last scale seen — consistent assumption

    for mark in marks:
        exam = mark.exam
        grade_letter = mark.grade
        scale = exam.grading_scale if exam else None

        if not scale or not grade_letter:
            continue

        try:
            grade_range = scale.grade_ranges.get(letter=grade_letter)
            total_points += float(grade_range.points)
            total_exams += 1
        except GradeRange.DoesNotExist:
            continue

    if total_exams == 0:
        return {
            "gpa": 0.0,
            "letter": "N/A",
            "grade_color": "bg-gray-400"
        }

    gpa = total_points / total_exams

    def color_for_gpa(gpa):
        if gpa >= 3.6:
            return "bg-green-600"
        elif gpa >= 3.0:
            return "bg-blue-600"
        elif gpa >= 2.0:
            return "bg-yellow-500"
        elif gpa >= 1.0:
            return "bg-orange-500"
        else:
            return "bg-red-600"

    grade_letter = scale.grade_ranges.filter(points__lte=gpa).order_by("-points").first()

    return {
        "gpa": round(gpa, 2),
        "letter": grade_letter.letter if grade_letter else "N/A",
        "grade_color": color_for_gpa(gpa)
    }
