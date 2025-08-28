from django.db import models
from django.conf import settings

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student')
    is_student = models.BooleanField(default=False)
    invitations = models.ManyToManyField("Teacher", related_name="student_invitations")

    def remove_invitations(self, teacher):
        self.invitations.remove(teacher)
        if teacher.invitations.all().contains(self):
            teacher.invitations.remove(self)

    def __str__(self):
        return self.user.username

class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher')
    students = models.ManyToManyField(Student, blank=True, related_name="teachers")
    is_teacher =  models.BooleanField(default=True)
    invitations = models.ManyToManyField("Student", related_name="teacher_invitations")

    def remove_invitations(self, student):
        self.invitations.remove(student)
        if student.invitations.all().contains(self):
            student.invitations.remove(self)

    def __str__(self):
        return self.user.username
