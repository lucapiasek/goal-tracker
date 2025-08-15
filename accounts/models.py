from django.db import models
from django.conf import settings

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, blank=True, on_delete=models.CASCADE)
    is_student = models.BooleanField(default=True)

class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, blank=True, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, blank=True, related_name="teachers")
    is_teacher =  models.BooleanField(default=True)
