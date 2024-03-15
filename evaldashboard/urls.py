"""evaldashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('add-mentor/', views.add_mentor, name='add_mentor'),
    path('add-student/', views.add_student, name='add_student'),
    path('mentors/<int:mentor_id>/', views.view_evaluations, name='view_evaluations'),
    path('mentors/<int:mentor_id>/add-student-mentor/', views.add_student_mentor, name='add_student_mentor'),
    path('mentors/<int:mentor_id>/evaluations/<int:evaluation_id>/assign-marks/', views.assign_marks, name='assign_marks'),
    path('mentors/<int:mentor_id>/evaluations/<int:evaluation_id>/remove-student/', views.remove_student, name='remove_student'),
    path('mentors/<int:mentor_id>/submit-marks/<int:evaluation_id>/', views.submit_marks, name='submit_marks'),
]
