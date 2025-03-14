from django.shortcuts import render, redirect
from .forms import PersonForm
from .models import Person

def index(request):
    return render(request, 'office/index.html')

def person_list(request):
    persons = Person.objects.all()
    return render(request, 'office/person_list.html', {'persons': persons})

def home(request):
    return render(request, 'office/home.html')

def add_person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('person_list')  # Fixed name
    else:
        form = PersonForm()
    return render(request, 'office/add_person.html', {'form': form})


def person_list(request):
    persons = Person.objects.all()
    return render(request, 'office/persons.html', {'persons': persons})