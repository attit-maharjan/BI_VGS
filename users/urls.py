# ====================================================================================
# 🌐 USERS APP URL CONFIGURATION
# ====================================================================================
# This module defines all URL routes related to the `users` app:
# - Authentication (login/logout)
# - Role-based dashboard redirects
# - Individual dashboards per role (admin, student, teacher sub-roles, etc.)
#
# NOTE:
#   - These views are imported from modularized view files inside `users/views/`
#   - This file uses a flat, centralized structure for clarity and simplicity
# ====================================================================================

from django.urls import path

# --------------------------------------------------------
# Import grouped views for clean modular access
# --------------------------------------------------------
from users.views import (
    auth_views, 
    dashboard_redirects,
    profile_views
)
from users.views.dashboards import (
    admin_views,
    principal_views,
    vice_principal_views,
    hod_views,
    classroom_teacher_views,
    subject_teacher_views,
    student_views,
    parent_views,
    fallback_views,
)



# Namespace for reversing URLs like 'users:login'
app_name = 'users'

# --------------------------------------------------------
# Define URL patterns
# --------------------------------------------------------
urlpatterns = [

    # ===============================
    # 🔐 Authentication
    # ===============================
    path('login/', auth_views.custom_login, name='login'),           # Custom email-based login
    path('logout/', auth_views.custom_logout, name='logout'),        # POST-only logout view

    # ===============================
    # 🚦 Dashboard Redirection Logic
    # ===============================
    path('dashboard/', dashboard_redirects.role_dashboard_redirect_view, name='role_dashboard'),     # Detects role and redirects
    path('fallback-dashboard/', fallback_views.fallback_dashboard, name='fallback_dashboard'),       # For unconfigured roles
    
    
    
    # ===============================
    # 👤 Profile Views
    # ===============================
    path('profile/', profile_views.view_profile, name='view_profile'),  # View profile page
    path('profile/edit/', profile_views.edit_profile, name='edit_profile'),  # Edit profile page
    # URL pattern for changing the user's password
    path('password/change/', profile_views.CustomPasswordChangeView.as_view(), name='change_password'),
    
    

    # ===============================
    # 🧑‍💼 Admin Dashboard
    # ===============================
    path('dashboard/admin/', admin_views.admin_dashboard, name='admin_dashboard'),
    path("dashboard/admin/register/", admin_views.admin_register_user_view, name="admin_register_user"),
    path("dashboard/admin/unassigned-students/", admin_views.unassigned_students_view, name="admin_unassigned_students"),
    path("dashboard/admin/unassigned-students/delete/<str:student_id>/", admin_views.delete_unassigned_student_view, name="delete_unassigned_student"),
    path("dashboard/admin/update-school-settings/", admin_views.admin_update_school_settings_view, name="admin_update_school_settings"),
    
    

    # ===============================
    # 🎓 Student Dashboard
    # ===============================
    path('dashboard/student/', student_views.student_dashboard, name='student_dashboard'),
    path('dashboard/student/subjects/', student_views.student_subjects_view, name='student_subjects'),
    path('dashboard/student/exams/', student_views.student_exam_schedule_view, name='student_exam_schedule'), 
    path("dashboard/student/results/summary/", student_views.exam_summary_view, name="student_exam_summary"),         # 📄 Table: Subject, Score, Grade
    path("dashboard/student/results/performance/", student_views.exam_performance_view, name="student_exam_performance"),  # 📊 Charts: Score vs Avg, Trend Line
    path("dashboard/student/results/insights/", student_views.exam_insights_view, name="student_exam_insights"),           # 📈 Grade Insight Bars
    path("dashboard/student/results/report-card/", student_views.exam_report_card_view, name="student_exam_report_card"),  # 🧾 Printable Report Card
    path("dashboard/student/results/comments/", student_views.exam_comments_view, name="student_exam_comments"),           # 💬 Smart Subject Comments
    path("dashboard/student/report-card/pdf/", student_views.exam_report_card_pdf_view, name="exam_report_card_pdf"),
    # student not enrolled completely:
    path('not-enrolled/', student_views.student_not_enrolled_view, name='student_not_enrolled'),




    # ===============================
    # 👨‍👩‍👧 Parent Dashboard
    # ===============================
    path('dashboard/parent/', parent_views.parent_dashboard, name='parent_dashboard'),
    path('dashboard/parent/child/<int:student_id>/', parent_views.parent_child_dashboard_view, name='parent_child_dashboard'),
    path('dashboard/parent/child/<int:student_id>/subjects/', parent_views.parent_child_subjects_view, name='parent_child_subjects'),
    path('dashboard/parent/child/<int:student_id>/exam-results/', parent_views.parent_child_exam_results_view, name='parent_child_exam_results'),
    path("dashboard/parent/child/<int:student_id>/exam-timetable/", parent_views.parent_child_exam_timetable_view, name="parent_child_exam_timetable"),
    path("dashboard/parent/child/<int:student_id>/grade-insights/", parent_views.parent_child_grade_insights_view, name="parent_child_grade_insights"),
    path('dashboard/parent/child/<int:student_id>/report-card/', parent_views.parent_child_report_card_view, name='my_child_report_card'),
    path("dashboard/parent/child/<int:student_id>/report-card/printable/", parent_views.parent_printable_report_card, name="parent_printable_report_card"),
    path('dashboard/parent/child/<int:student_id>/performance/', parent_views.parent_child_performance_view, name='parent_child_performance'),
    path("dashboard/parent/child/<int:student_id>/subject-comments/", parent_views.parent_subject_comments_view, name="parent_subject_comments"),
    path("dashboard/parent/child/<int:student_id>/teacher-contacts/", parent_views.parent_contact_teachers_view, name="parent_teacher_contacts"),






    
    

    # ===============================
    # 🧑‍🏫 Main Teacher Dashboards (Sub-Roles)
    # ===============================
    path('dashboard/principal/', principal_views.principal_dashboard, name='principal_dashboard'),
    path('dashboard/vice-principal/', vice_principal_views.vice_principal_dashboard, name='vice_principal_dashboard'),
    path('dashboard/hod/', hod_views.hod_dashboard, name='hod_dashboard'),
    path('dashboard/classroom-teacher/', classroom_teacher_views.classroom_teacher_dashboard, name='classroom_teacher_dashboard'),
    path('dashboard/subject-teacher/', subject_teacher_views.subject_teacher_dashboard, name='subject_teacher_dashboard'),
    
    
    
    # ===============================
    # 🧑‍🏫 Classroom Teacher Subviews
    # ===============================
    path('dashboard/classroom-teacher/students/', classroom_teacher_views.classroom_teacher_view_student_view, name="classroom_students"),
    path('dashboard/classroom-teacher/charts/', classroom_teacher_views.classroom_teacher_student_charts_view, name='classroom_teacher_charts'),
    path("dashboard/classroom-teacher/subject-performance/", classroom_teacher_views.classroom_teacher_view_subject_performance, name="classroom_teacher_view_subject_performance"),
    
    # ✅ 1. CLASSROOM TEACHER EXTENSIONS
    # ----------------------------------------------------
    path('dashboard/classroom-teacher/student/<int:student_id>/', classroom_teacher_views.classroom_teacher_view_studenthub_dashboard, name='classroom_teacher_studenthub'),
    path('dashboard/classroom-teacher/student/<int:student_id>/subjects/', classroom_teacher_views.classroom_teacher_student_subjects_view, name='classroom_teacher_student_subjects'),
    path('dashboard/classroom-teacher/student/<int:student_id>/exam-results/', classroom_teacher_views.classroom_teacher_exam_results_view, name='classroom_teacher_exam_results'),
    path('dashboard/classroom-teacher/student/<int:student_id>/exam-timetable/', classroom_teacher_views.classroom_teacher_exam_timetable_view, name='classroom_teacher_exam_timetable'),
    path('dashboard/classroom-teacher/student/<int:student_id>/grade-insights/', classroom_teacher_views.classroom_teacher_grade_insights_view, name='classroom_teacher_grade_insights'),
    path('dashboard/classroom-teacher/student/<int:student_id>/report-card/', classroom_teacher_views.classroom_teacher_report_card_view, name='classroom_teacher_report_card'),
    path('dashboard/classroom-teacher/student/<int:student_id>/report-card/printable/', classroom_teacher_views.classroom_teacher_printable_report_card, name='classroom_teacher_printable_report_card'),
    path('dashboard/classroom-teacher/student/<int:student_id>/performance/', classroom_teacher_views.classroom_teacher_performance_view, name='classroom_teacher_performance'),
    path('dashboard/classroom-teacher/student/<int:student_id>/subject-comments/', classroom_teacher_views.classroom_teacher_subject_comments_view, name='classroom_teacher_subject_comments'),
    path('dashboard/classroom-teacher/student/<int:student_id>/teacher-contacts/', classroom_teacher_views.classroom_teacher_contact_teachers_view, name='classroom_teacher_teacher_contacts'),
    
    
    
    
    
    # ===============================
    # 🧑‍🏫 Subject Teacher Subviews
    # ===============================    
    path("dashboard/subject-teacher/subject-performance/", subject_teacher_views.subject_teacher_view_subject_performance, name="subject_teacher_view_subject_performance"),
    path("dashboard/subject-teacher/students/", subject_teacher_views.subject_teacher_view_student_view, name="subject_students"),
    path('dashboard/subject-teacher/student/<int:student_id>/', subject_teacher_views.subject_teacher_view_studenthub_dashboard, name='subject_teacher_studenthub'),
    path("dashboard/subject-teacher/charts/", subject_teacher_views.subject_teacher_student_charts_view, name="subject_teacher_view_charts"),
    
    # ===============================
    # 🧑‍🏫 Subject Teacher CRUD Views
    # ===============================
    path("dashboard/subject-teacher/exam/<int:exam_id>/update-marks/", subject_teacher_views.update_exam_marks_view, name="update_exam_marks"),
    path('dashboard/subject-teacher/exams/select/', subject_teacher_views.select_exam_for_mark_update_view, name='select_exam_for_mark_update'),

        
    # ✅ 2. SUBJECT TEACHER EXTENSIONS
    # ----------------------------------------------------
    path('dashboard/subject-teacher/student/<int:student_id>/subjects/', subject_teacher_views.subject_teacher_student_subjects_view, name='subject_teacher_student_subjects'),
    path('dashboard/subject-teacher/student/<int:student_id>/exam-results/', subject_teacher_views.subject_teacher_exam_results_view, name='subject_teacher_exam_results'),
    path('dashboard/subject-teacher/student/<int:student_id>/exam-timetable/', subject_teacher_views.subject_teacher_exam_timetable_view, name='subject_teacher_exam_timetable'),
    path('dashboard/subject-teacher/student/<int:student_id>/grade-insights/', subject_teacher_views.subject_teacher_grade_insights_view, name='subject_teacher_grade_insights'),
    path('dashboard/subject-teacher/student/<int:student_id>/report-card/', subject_teacher_views.subject_teacher_report_card_view, name='subject_teacher_report_card'),
    path('dashboard/subject-teacher/student/<int:student_id>/report-card/printable/', subject_teacher_views.subject_teacher_printable_report_card, name='subject_teacher_printable_report_card'),
    path('dashboard/subject-teacher/student/<int:student_id>/performance/', subject_teacher_views.subject_teacher_performance_view, name='subject_teacher_performance'),
    path('dashboard/subject-teacher/student/<int:student_id>/subject-comments/', subject_teacher_views.subject_teacher_subject_comments_view, name='subject_teacher_subject_comments'),
    path('dashboard/subject-teacher/student/<int:student_id>/teacher-contacts/', subject_teacher_views.subject_teacher_contact_teachers_view, name='subject_teacher_teacher_contacts'),
  
  
    
    
    # ===============================
    # 🏛️ HOD Subviews
    # ===============================
    path("dashboard/hod/subject-performance/", hod_views.hod_view_subject_performance, name="hod_view_subject_performance"),
    path("dashboard/hod/dept-current-students/", hod_views.hod_view_student_view, name="hod_students"),
    path('dashboard/hod/student/<int:student_id>/',  hod_views.hod_view_studenthub_dashboard, name='hod_studenthub'),
    path("dashboard/hod/subjects/charts/", hod_views.hod_student_charts_view, name="hod_view_subject_charts"),

    # ✅ 3. HOD EXTENSIONS
    # ----------------------------------------------------
    path('dashboard/hod/student/<int:student_id>/subjects/', hod_views.hod_student_subjects_view, name='hod_student_subjects'),
    path('dashboard/hod/student/<int:student_id>/exam-results/', hod_views.hod_exam_results_view, name='hod_exam_results'),
    path('dashboard/hod/student/<int:student_id>/exam-timetable/', hod_views.hod_exam_timetable_view, name='hod_exam_timetable'),
    path('dashboard/hod/student/<int:student_id>/grade-insights/', hod_views.hod_grade_insights_view, name='hod_grade_insights'),
    path('dashboard/hod/student/<int:student_id>/report-card/', hod_views.hod_report_card_view, name='hod_report_card'),
    path('dashboard/hod/student/<int:student_id>/report-card/printable/', hod_views.hod_printable_report_card, name='hod_printable_report_card'),
    path('dashboard/hod/student/<int:student_id>/performance/', hod_views.hod_performance_view, name='hod_performance'),
    path('dashboard/hod/student/<int:student_id>/subject-comments/', hod_views.hod_subject_comments_view, name='hod_subject_comments'),
    path('dashboard/hod/student/<int:student_id>/teacher-contacts/', hod_views.hod_contact_teachers_view, name='hod_teacher_contacts'),
    
    
    
    
    
    
    # ===============================
    # 👨‍💼 Vice Principal Subviews
    # ===============================
    path("dashboard/vp/subject-performance/", vice_principal_views.vice_principal_view_subject_performance, name="vice_principal_view_subject_performance"),
    path("dashboard/vp/all-current-students/", vice_principal_views.vice_principal_view_student_view, name="vp_students"),    
    path('dashboard/vp/student/<int:student_id>/', vice_principal_views.vice_principal_view_studenthub_dashboard, name='vice_principal_studenthub'),  
    path("dashboard/vice-principal/school-wide/charts/", vice_principal_views.vice_principal_student_charts_view, name="vice_principal_view_student_charts"),

    # ✅ 4. VICE PRINCIPAL EXTENSIONS
    # ----------------------------------------------------
    path('dashboard/vp/student/<int:student_id>/subjects/', vice_principal_views.vice_principal_student_subjects_view, name='vice_principal_student_subjects'),
    path('dashboard/vp/student/<int:student_id>/exam-results/', vice_principal_views.vice_principal_exam_results_view, name='vice_principal_exam_results'),
    path('dashboard/vp/student/<int:student_id>/exam-timetable/', vice_principal_views.vice_principal_exam_timetable_view, name='vice_principal_exam_timetable'),
    path('dashboard/vp/student/<int:student_id>/grade-insights/', vice_principal_views.vice_principal_grade_insights_view, name='vice_principal_grade_insights'),
    path('dashboard/vp/student/<int:student_id>/report-card/', vice_principal_views.vice_principal_report_card_view, name='vice_principal_report_card'),
    path('dashboard/vp/student/<int:student_id>/report-card/printable/', vice_principal_views.vice_principal_printable_report_card, name='vice_principal_printable_report_card'),
    path('dashboard/vp/student/<int:student_id>/performance/', vice_principal_views.vice_principal_performance_view, name='vice_principal_performance'),
    path('dashboard/vp/student/<int:student_id>/subject-comments/', vice_principal_views.vice_principal_subject_comments_view, name='vice_principal_subject_comments'),
    path('dashboard/vp/student/<int:student_id>/teacher-contacts/', vice_principal_views.vice_principal_contact_teachers_view, name='vice_principal_teacher_contacts'),




    # ===============================
    # 🏫 Principal Subviews
    # ===============================
    path("dashboard/principal/subject-performance/", principal_views.principal_view_subject_performance, name="principal_view_subject_performance"),
    path("dashboard/principal/all-current-students/", principal_views.principal_view_student_view, name="principal_students"),
    path('dashboard/principal/student/<int:student_id>/', principal_views.principal_view_studenthub_dashboard, name='principal_studenthub'),
    path("dashboard/principal/school-wide/charts/", principal_views.principal_student_charts_view, name="principal_view_charts"),

    # ✅ 5. PRINCIPAL EXTENSIONS
    # ----------------------------------------------------
    path('dashboard/principal/student/<int:student_id>/subjects/', principal_views.principal_student_subjects_view, name='principal_student_subjects'),
    path('dashboard/principal/student/<int:student_id>/exam-results/', principal_views.principal_exam_results_view, name='principal_exam_results'),
    path('dashboard/principal/student/<int:student_id>/exam-timetable/', principal_views.principal_exam_timetable_view, name='principal_exam_timetable'),
    path('dashboard/principal/student/<int:student_id>/grade-insights/', principal_views.principal_grade_insights_view, name='principal_grade_insights'),
    path('dashboard/principal/student/<int:student_id>/report-card/', principal_views.principal_report_card_view, name='principal_report_card'),
    path('dashboard/principal/student/<int:student_id>/report-card/printable/', principal_views.principal_printable_report_card, name='principal_printable_report_card'),
    path('dashboard/principal/student/<int:student_id>/performance/', principal_views.principal_performance_view, name='principal_performance'),
    path('dashboard/principal/student/<int:student_id>/subject-comments/', principal_views.principal_subject_comments_view, name='principal_subject_comments'),
    path('dashboard/principal/student/<int:student_id>/teacher-contacts/', principal_views.principal_contact_teachers_view, name='principal_teacher_contacts'),
    
]

