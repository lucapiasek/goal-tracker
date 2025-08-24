from django.contrib.auth import get_user_model, get_user
from django.shortcuts import get_object_or_404

UserModel = get_user_model()

def is_owner(user, username):
    owner = get_object_or_404(UserModel, username=username)
    return user == owner

def is_teacher(user, username):
    owner = get_object_or_404(UserModel, username=username)
    if user != owner:
        if hasattr(user, 'teacher'):
            if user.teacher.is_teacher:
                students = user.teacher.students.all()
                return students.contains(owner.student)
        return False
    return False

def is_owner_or_is_teacher(user, username):
    return is_owner(user, username) or is_teacher(user, username)

def is_student(user, username):
    owner = get_object_or_404(UserModel, username=username)
    if user != owner:
        if hasattr(owner, 'student'):
            if user.teacher.is_teacher:
                students = user.teacher.students.all()
                return students.contains(owner.student)
        return False
    return False
