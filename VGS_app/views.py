from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from .forms import PersonForm
from .models import Person, Role, StudentDetails, TeacherDetails, ParentStudent, AcademicYear, Class, Subject, ClassSubject, StudentEnrollment, Grade, ReportCardSnapshot, User, AcademicEvent
from django.contrib.auth.models import User
import calendar
from datetime import datetime
import json

def index(request):
    return render(request, 'VGS_app/index.html')

def person_list(request):
    persons = Person.objects.all()
    return render(request, 'VGS_app/person_list.html', {'persons': persons})

def home(request):
    return render(request, 'VGS_app/home.html')

def add_person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('person_list')  # Fixed name
    else:
        form = PersonForm()
    return render(request, 'VGS_app/add_person.html', {'form': form})

def person_list(request):
    persons = Person.objects.all()
    return render(request, 'VGS_app/persons.html', {'persons': persons})

def home_view(request):
    return HttpResponse("Hello, this is the home page!")

def about(request):
    return render(request, 'VGS_app/about.html')

def academics(request):
    return render(request, 'VGS_app/academics.html')

def admissions(request):
    return render(request, 'VGS_app/admissions.html')

def contact(request):
    return render(request, 'VGS_app/contact.html')

def calendar_view(request):
    # Create a list of months with their respective days
    months = []
    for month_num in range(1, 13):  # Loop through the months (1 to 12)
        month_name = calendar.month_name[month_num]  # Get month name
        month_days = []
        
        # Get the days of the month (use the calendar module to get a list of days)
        _, num_days = calendar.monthrange(2025, month_num)  # Get the number of days in the month for the year 2025
        week = []
        for day in range(1, num_days + 1):
            week.append(day)
            if len(week) == 7:  # If the week has 7 days, push it to month_days and start a new week
                month_days.append(week)
                week = []
        if week:  # If there are leftover days, append the last week
            month_days.append(week)
        
        months.append({
            'month_name': month_name,
            'month': month_num,
            'month_days': month_days
        })
    
    # Example events data
    events = [
        {'date': '2025-03-10', 'title': 'Event 1', 'description': 'Description of Event 1', 'event_type': 'Lecture'},
        {'date': '2025-03-15', 'title': 'Event 2', 'description': 'Description of Event 2', 'event_type': 'Workshop'}
    ]

    # Pass the months and events data to the template
    context = {
        'events': events,
        'current_year': 2025,
        'months': months
    }
    
    return render(request, 'calendar.html', context)

from django.shortcuts import render

def career_view(request):
    return render(request, 'career.html')
