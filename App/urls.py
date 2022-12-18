from django.urls import path
from django.urls.conf import re_path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from App import views

app_name = 'App'

urlpatterns = [
    # Instructors 
    
    path('instructorslist', views.instructors_list, name='instructorslist'),
    path('instructordetails/<int:id>', views.instructor_details, name='instructordetails'),
    path('instructoredit/<int:id>', views.instructor_edit, name='instructoredit'),
    path('instructordelete/<int:id>', views.instructor_delete, name='instructordelete'),
    
    
    # Structures
    
    path('structureslist', views.structures_list, name='structureslist'),
    path('structuredetails/<int:id>', views.structure_details, name='structuredetails'),
    path('structureedit/<int:id>', views.structure_edit, name='structureedit'),
    path('structuredelete/<int:id>', views.structure_delete, name='structuredelete'),
    
    # Courses
    path('courseslist/', views.courses_list, name='courseslist'),
    path('courseedit/<int:id>/<int:pk>', views.course_edit, name='courseedit'),
    path('coursedelete/<int:id>/<int:pk>', views.course_delete, name='coursedelete'),
    
    # Programs 
    
    path('programslist', views.programs_list, name='programslist'),
    path('programdetails/<int:id>', views.program_details, name='programdetails'),
    path('programedit/<int:id>', views.program_edit, name='programedit'),
    path('programdelete/<int:id>', views.program_delete, name='programdelete'),
    
    # program second test pour l'affichage des instructeurs
    path('programdetailstest/<int:id>', views.programdetailstest, name='programdetailstest'),
    
    # Tasks for a program
    path('taskcreate/<int:id>', views.task_create, name='taskcreate'),
    path('taskedit/<int:id>/<int:pk>', views.task_edit, name='taskedit'),
    path('taskelete/<int:id>/<int:pk>', views.task_delete, name='taskelete'),
    
    path('proginsdetails/<int:id>/<int:pk>/', views.proginsdetails, name='proginsdetails'),
    path('progcalendarmodify/<int:id>/', views.modify_prog_calendar, name='progcalendarmodify'),
    
    
    path('programdateedit/<int:id>/<int:pk>', views.program_date_edit, name='programdateedit'),  
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)