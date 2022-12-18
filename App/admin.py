from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Instructor)
admin.site.register(Course)
admin.site.register(Structure)
admin.site.register(Program)
admin.site.register(ProgramDate)
admin.site.register(InstructorProgram)
admin.site.register(Task)