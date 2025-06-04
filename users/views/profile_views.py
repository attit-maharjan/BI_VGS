# ************************
#  users > views > profile_views.py
# ************************

# ============================
#  IMPORTS
# ============================
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from users.forms import UserUpdateForm


# ============================
#  Edit Profile View
# ============================
@login_required
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            if form.has_changed():
                form.save()
                messages.success(request, "Your profile was updated successfully.")
                return redirect('users:view_profile')
            else:
                messages.info(request, "No changes detected.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserUpdateForm(instance=user)

    return render(request, 'users/accounts/edit_profile.html', {'form': form})


# ============================
#  View Profile Page
# ============================
@login_required
def view_profile(request):
    user = request.user
    return render(request, 'users/accounts/view_profile.html', {'user': user})


# ============================
#  Password Change View
# ============================
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'users/accounts/change_password.html'
    success_url = reverse_lazy('users:view_profile')
