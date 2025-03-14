from django.urls import path
from . import views  # Import views from your app

urlpatterns = [
    path('vgs', views.index, name='index'),  # Index page
    path('vsghome/', views.home, name='home'),  # Home page
    path('home_view/', views.home_view, name='home_view'),  # Another home view (simple HttpResponse)
    path('person_list/', views.person_list, name='person_list'),  # List of persons
    path('add_person/', views.add_person, name='add_person'),  # Add a new person
    path('about/', views.about, name='about'),  # About page
    path('academics/', views.academics, name='academics'),  # Academics page
    path('admissions/', views.admissions, name='admissions'),  # Admissions page
    path('contact/', views.contact, name='contact'),  # Contact page
    path('calendar/', views.calendar_view, name='calendar'),  # Calendar page
    path('career/', views.career_view, name='career'),  # Career page
]
