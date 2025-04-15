from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import Person
from django import forms

class CustomLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

@csrf_protect
def custom_login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'school/login.html')

@login_required
def dashboard(request):
    try:
        person = Person.objects.get(email=request.user.email)
        role = person.role
        context = {
            'person': person,
            'role': role
        }
        return render(request, 'school/dashboard.html', context)
    except Person.DoesNotExist:
        return redirect('login')

@login_required
def home_view(request):
    return render(request, 'school/home.html')  # Render the home page template

def home(request):
    return render(request, 'school/base.html')  # Render the base template


