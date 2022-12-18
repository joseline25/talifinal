from django import forms
from .models import Instructor, Program, Course, InstructorProgram, Structure, ProgramDate, Task

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        exclude = ['instructors']

        widgets = {
            'start_date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'placeholder': 'Select a '
                                                                                                            'date',
                                                                    'type': 'date'}) ,
            'end_date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'placeholder': 'Select a '
                                                                                                            'date',
                                                                    'type': 'date'}),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ['program', 'added_date']
        widgets = {
            'start_date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'placeholder': 'Select a '
                                                                                                            'date',
                                                                    'type': 'date'}) ,
            'end_date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'placeholder': 'Select a '
                                                                                                            'date',
                                                                    'type': 'date'}),
        }
       
        
class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = "__all__"
        
        
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ['instructors']
        

class StructureForm(forms.ModelForm):
    class Meta:
        model = Structure
        exclude = ['courses']
        
class InstructorProgramForm(forms.ModelForm):
    class Meta:
        model = InstructorProgram
        fields = ['instructor']
        
class ProgramDateForm(forms.ModelForm):
    class Meta:
        model = ProgramDate
        fields = ['course_date']
        
        widgets = {
            'course_date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'placeholder': 'Select a '
                                                                                                            'date',
                                                                    'type': 'date'}) ,
        }
        
       
        