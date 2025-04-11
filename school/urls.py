from django.urls import path
from django.contrib.auth import views as auth_views
from .views import custom_login_view, home_view

urlpatterns = [
    path('', home_view, name='home'),  # Added home page URL
    path('login/', custom_login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='school/login.html', next_page='login'), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='school/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='school/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='school/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='school/password_reset_complete.html'), name='password_reset_complete'),
]
