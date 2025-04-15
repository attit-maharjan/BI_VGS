from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
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
            login(request, user)  # Correctly calls Django's login function
            return redirect('school:dashboard')  # Redirect to the dashboard
    return render(request, 'school/login.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)  # Correctly calls Django's login function
            return redirect('school:dashboard')  # Redirect to the dashboard
    return render(request, 'school/login.html') 

@login_required
def dashboard(request):
    try:
        person = Person.objects.get(email=request.user.email)
        # Redirect based on role
        if person.role == 'Teacher':
            return redirect('school:teacher_dashboard')
        elif person.role == 'parent':
            return redirect('school:parent_dashboard')
        elif person.role == 'admin':
            return redirect('school:admin_dashboard')
        else:
            # Handle unknown roles or add more roles as needed
            return redirect('school:student_dashboard')
    
    except Person.DoesNotExist:
        # Handle case where Person record doesn't exist
        return redirect('school:login')

# Add these new dashboard views
@login_required
def teacher_dashboard(request):
    context = {'user': request.user}
    return render(request, 'school/teacher_dashboard.html', context)

@login_required
def student_dashboard(request):
    context = {'user': request.user}
    return render(request, 'school/student_dashboard.html', context)

@login_required
def staff_dashboard(request):
    context = {'user': request.user}
    return render(request, 'school/staff_dashboard.html', context)

@login_required
def home_view(request):
    return render(request, 'school/home.html')  # Render the home page template

def home(request):
    return render(request, 'school/base.html')  # Render the base template
def about(request):
    return render(request, 'school/about.html')  # Render the about page template
def contact(request):
    return render(request, 'school/contact.html')  # Render the contact page template   
def index(request):
    return render(request, 'school/index.html')  # Render the index page template


def student_login(request):
    if request.method == 'POST':
        student_email = request.POST.get('username')  # Email is used as the username
        password = request.POST.get('password')
        print(f"Attempting login for email: {student_email}")  # Debug print

        # Authenticate using email and password
        user = authenticate(request, username=student_email, password=password)  # Authenticate using email
        if user is not None:
            print("Authentication successful")  # Debug print
            login(request, user)  # This now correctly calls Django's auth.login
            return redirect('school:student_dashboard')  # Redirect to student dashboard
        else:
            print("Authentication failed")  # Debug print
            return render(request, 'school/student_login.html', {'error': 'Invalid email or password'})
    return render(request, 'school/student_login.html')

def teacher_login(request):
    if request.method == 'POST':
        teacher_email = request.POST.get('username')
        password = request.POST.get('password')
        print(f"Teacher login attempt: {teacher_email}")

        user = authenticate(request, username=teacher_email, password=password)
        if user is not None:
            # Add role check (example: check groups or custom user field)
            if user.is_teacher:  # Replace with your actual role check
                login(request, user)
                return redirect('school:teacher_dashboard')
            else:
                return render(request, 'school/teacher_login.html', {'error': 'Not authorized as teacher'})
        else:
            return render(request, 'school/teacher_login.html', {'error': 'Invalid credentials'})
    return render(request, 'school/teacher_login.html')

def parent_login(request):
    if request.method == 'POST':
        parent_email = request.POST.get('username')
        password = request.POST.get('password')
        print(f"Parent login attempt: {parent_email}")

        user = authenticate(request, username=parent_email, password=password)
        if user is not None:
            if user.is_parent:  # Replace with your role check
                login(request, user)
                return redirect('school:parent_dashboard')
            else:
                return render(request, 'school/parent_login.html', {'error': 'Not authorized as parent'})
        else:
            return render(request, 'school/parent_login.html', {'error': 'Invalid credentials'})
    return render(request, 'school/parent_login.html')

def admin_login(request):
    if request.method == 'POST':
        admin_email = request.POST.get('username')
        password = request.POST.get('password')
        print(f"Admin login attempt: {admin_email}")

        user = authenticate(request, username=admin_email, password=password)
        if user is not None:
            if user.is_superuser:  # Built-in Django admin check
                login(request, user)
                return redirect('school:admin_dashboard')
            else:
                return render(request, 'school/admin_login.html', {'error': 'Not authorized as admin'})
        else:
            return render(request, 'school/admin_login.html', {'error': 'Invalid credentials'})
    return render(request, 'school/admin_login.html')

def stakeholder_login(request):
    if request.method == 'POST':
        stakeholder_email = request.POST.get('username')
        password = request.POST.get('password')
        print(f"Stakeholder login attempt: {stakeholder_email}")

        user = authenticate(request, username=stakeholder_email, password=password)
        if user is not None:
            if user.is_stakeholder:  # Replace with your role check
                login(request, user)
                return redirect('school:stakeholder_dashboard')
            else:
                return render(request, 'school/stakeholder_login.html', {'error': 'Not authorized as stakeholder'})
        else:
            return render(request, 'school/stakeholder_login.html', {'error': 'Invalid credentials'})
    return render(request, 'school/stakeholder_login.html')

def staff_login(request):
    if request.method == 'POST':
        staff_email = request.POST.get('username')
        password = request.POST.get('password')
        print(f"Staff login attempt: {staff_email}")

        user = authenticate(request, username=staff_email, password=password)
        if user is not None:
            if user.is_staff:  # Built-in Django staff check
                login(request, user)
                return redirect('school:teacher_dashboard')  # Redirect to staff dashboard
            else:
                return render(request, 'school/staff_login.html', {'error': 'Not authorized as staff'})
        else:
            return render(request, 'school/staff_login.html', {'error': 'Invalid credentials'})
    return render(request, 'school/staff_login.html')

@login_required
def student_dashboard(request):
    # Example data for the dashboard
    schedule = [
        {'day': 'Monday', 'classes': [{'time': '9:00 AM', 'subject': 'Math', 'room': '101'}, {'time': '11:00 AM', 'subject': 'Science', 'room': '102'}]},
        {'day': 'Tuesday', 'classes': [{'time': '10:00 AM', 'subject': 'English', 'room': '103'}, {'time': '1:00 PM', 'subject': 'History', 'room': '104'}]},
    ]

    assignments = [
        {'id': 1, 'subject': 'Math', 'description': 'Complete Chapter 5', 'due_date': '2025-04-10', 'submitted': False},
        {'id': 2, 'subject': 'Science', 'description': 'Lab Report on Experiment 3', 'due_date': '2025-04-12', 'submitted': True, 'submission_date': '2025-04-08'},
    ]

    results = [
        {'subject': 'Math', 'marks': 95, 'grade': 'A', 'rank': 1},
        {'subject': 'Science', 'marks': 88, 'grade': 'B+', 'rank': 3},
        {'subject': 'English', 'marks': 92, 'grade': 'A-', 'rank': 2},
    ]

    context = {
        'user': request.user,
        'student_class': '10th Grade',  # Example data
        'enrollment_number': request.user.email,  # Use the email as enrollment number
        'schedule': schedule,
        'assignments': assignments,
        'results': results,
    }

    return render(request, 'school/student_dashboard.html', context)

def teacher_dashboard(request):
    # Example dashboard view
    return render(request, 'school/teacher_dashboard.html')

def parent_dashboard(request):
    return render(request, 'school/parent_dashboard.html')

def admin_dashboard(request):
    return render(request, 'school/admin_dashboard.html')

def stakeholder_dashboard(request):
    total_students = 100  # Example value
    total_staff = 20  # Example value
    subject_list = ['Math', 'Science', 'English']  # Example list
    attendance_list = [80, 90, 85]  # Example list

    context = {
        'total_students': total_students,
        'total_staff': total_staff,
        'subject_list': mark_safe(json.dumps(subject_list)),
        'attendance_list': mark_safe(json.dumps(attendance_list)),
        'page_title': 'Stakeholder Dashboard',
        'chart_js': '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>'
    }
    return render(request, 'school/stakeholder_dashboard.html', context)

def staff_dashboard(request):
    return render(request, 'school/staff_dashboard.html')


def logout_view(request):
    """Logs out the user and redirects to the homepage."""
    logout(request)
    return redirect('school:index')  # Redirect to the homepage after logout

def some_view(request):
    logout_url = reverse('school:logout')
    return redirect(logout_url)

def events(request):
    return render(request, 'school/events.html')


def custom_404_view(request, exception):
    """Custom 404 error handler."""
    return render(request, '404.html', status=404)



def trigger_404(request):
    """View to intentionally trigger a 404 error."""
    raise Http404("404.html")

def academics(request):
    return render(request, 'school/academics.html')  # Render the academics page template
def admissions(request):
    return render(request, 'school/admissions.html')  # Render the admissions page template
def career(request):
    return render(request, 'school/career.html')  # Render the career page template
def calendar(request):
    return render(request, 'school/calendar.html')  # Render the calendar page template
def password_reset(request):
    return render(request, 'school/password_reset.html')  # Render the password reset page template