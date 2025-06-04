"""
users/views/auth_views.py

Handles:
- Custom email-based login
- Secure POST-based logout
"""

from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.messages import get_messages

from users.forms import EmailAuthenticationForm


# =====================================================
# 🔐 Custom Login View
# =====================================================
def custom_login(request):
    """
    Log in users using email + password.
    Supports 'Remember Me' and session expiry control.
    Redirects authenticated users to their role dashboard.
    """
    if request.user.is_authenticated:
        return redirect('users:role_dashboard')

    form = EmailAuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Clear stale messages like "logged out"
            list(get_messages(request))

            # Handle session expiry based on Remember Me
            if not form.cleaned_data.get('remember_me'):
                request.session.set_expiry(0)  # Session ends on browser close
            else:
                request.session.set_expiry(60 * 60 * 24 * 30)  # 30 days

            messages.success(request, f"✅ Welcome back, {user.get_short_name()}!")
            return redirect('users:role_dashboard')
        else:
            messages.error(request, "❌ Invalid email or password. Please try again.")

    return render(request, 'users/accounts/login.html', {'form': form})


# =====================================================
# 🚪 Custom Logout View
# =====================================================
@require_POST
@login_required
def custom_logout(request):
    """
    Log out user securely via POST.
    """
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('users:login')
