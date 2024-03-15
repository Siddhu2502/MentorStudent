from django.contrib import admin
from .models import Mentor, Student, Evaluation

admin.site.register(Mentor)
admin.site.register(Student)
admin.site.register(Evaluation)