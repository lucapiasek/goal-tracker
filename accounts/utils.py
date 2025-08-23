from .models import Student, Teacher

def if_not_student_create(user):
    if not hasattr(user, 'student'):
        student = Student(user=user)
        student.save()
        user.student = student
        user.save()

def if_not_teacher_create(user):
    if not hasattr(user, 'teacher'):
        teacher = Teacher(user=user)
        teacher.save()
        user.teacher = teacher
        user.save()