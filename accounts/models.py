from django.db import models
from django.conf import settings

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student')
    is_student = models.BooleanField(default=False)
    invitations = models.ManyToManyField("Teacher", related_name="student_invitations")

class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher')
    students = models.ManyToManyField(Student, blank=True, related_name="teachers")
    is_teacher =  models.BooleanField(default=False)
    invitations = models.ManyToManyField("Student", related_name="teacher_invitations")
