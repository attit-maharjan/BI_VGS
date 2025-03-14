from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='office/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
   
    path('person/', views.person_list, name='person_list'),
    path('add_person/', views.add_person, name='add_person'),


]
