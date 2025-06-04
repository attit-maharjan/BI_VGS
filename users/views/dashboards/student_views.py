# *******************************
# users > views > dashboards > student_views.py
# *******************************

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.http import HttpResponse
from django.contrib import messages



from xhtml2pdf import pisa

from users.helpers.generate_chart_images import generate_grade_distribution_charts
from users.services.student_dashboard_service import (
    get_student_dashboard_summary,
    get_student_subjects,
    get_student_exam_schedule,
)
from users.services.context.student_exam_context_service import (
    get_exam_summary_context,
    get_exam_performance_context,
    get_exam_insights_context,
    get_exam_report_card_context,
    get_exam_comments_context,
)

from enrollments.models import ClassGroupStudentEnrollment


# ===============================================
# 📊 DASHBOARD + SUBJECTS + TIMETABLE
# ===============================================

@login_required
def student_dashboard(request):
    student = request.user.student
    context = get_student_dashboard_summary(student)
    return render(request, 'dashboards/student/student_dashboard.html', context)


@login_required
def student_subjects_view(request):
    student = request.user.student
    context = get_student_subjects(student)
    return render(request, 'dashboards/student/student_subjects.html', context)


@login_required
def student_exam_schedule_view(request):
    student = request.user.student
    context = get_student_exam_schedule(student)
    return render(request, 'dashboards/student/student_exam_schedule.html', context)


# ===============================================
# 🧪 EXAM DATA VIEWS
# ===============================================

@login_required
def exam_summary_view(request):
    student = request.user.student
    context = get_exam_summary_context(student)
    return render(request, 'dashboards/student/exam_summary.html', context)


@login_required
def exam_performance_view(request):
    student = request.user.student
    context = get_exam_performance_context(student)
    return render(request, 'dashboards/student/exam_performance.html', context)


@login_required
def exam_insights_view(request):
    student = request.user.student
    context = get_exam_insights_context(student)
    return render(request, 'dashboards/student/exam_insights.html', context)



@login_required
def exam_report_card_view(request):
    student = request.user.student

    # ❗ Prevent crash when student has no class group enrollment
    try:
        ClassGroupStudentEnrollment.objects.get(student=student)
    except ClassGroupStudentEnrollment.DoesNotExist:
        messages.error(request, "You are not yet assigned to a class group. Report card unavailable.")
        return redirect("users:student_dashboard")

    context = get_exam_report_card_context(student)
    return render(request, 'dashboards/student/exam_report_card.html', context)





# =============================
# 📘 View: Student Subject Comments
# =============================
@login_required
def exam_comments_view(request):
    student = request.user.student
    context = get_exam_comments_context(student)
    return render(request, 'dashboards/student/exam_comments.html', context)




# ===============================================
# 🧾 PDF EXPORT: REPORT CARD
# ===============================================

@login_required
def exam_report_card_pdf_view(request):
    student = request.user.student

    # Defensive check: Ensure the student has a class group enrollment
    try:
        ClassGroupStudentEnrollment.objects.get(student=student)
    except ClassGroupStudentEnrollment.DoesNotExist:
        messages.error(request, "You are not yet assigned to any class group. Please contact the administrator.")
        return redirect("users:student_dashboard")

    context = get_exam_report_card_context(student)
    context["report_chart_images"] = generate_grade_distribution_charts(context["report_card"])
    context["user"] = request.user

    template = get_template("dashboards/student/pdf/pdf_report_card_template.html")
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report_card.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("PDF generation failed", status=500)

    return response



# -------------------------------------
# 🚫 Not Enrolled View (Shared Error Page)
# -------------------------------------

@login_required
def student_not_enrolled_view(request):
    return render(request, "dashboards/student/not_enrolled/student_not_enrolled.html")
