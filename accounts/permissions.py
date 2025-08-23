from django.contrib.auth import get_user_model, get_user
from django.shortcuts import get_object_or_404

UserModel = get_user_model()

def is_owner(request, username):
    owner = get_object_or_404(UserModel, username=username)
    return request.user == owner

def is_teacher(request, username):
    owner = get_object_or_404(UserModel, username=username)
    if request.user != owner:
        user = get_user(request)
        if hasattr(user, 'teacher') and hasattr(owner, 'student'):
            if user.teacher.is_teacher:
                students = user.teacher.students.all()
                return students.contains(owner.student)
        return False
    return False


def is_owner_or_is_teacher(request, username):
    return is_owner or is_teacher
