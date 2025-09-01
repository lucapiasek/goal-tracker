import pytest
from django.test import Client
from .models import Student, Teacher
from django.contrib.auth import get_user_model

UserModel = get_user_model()


@pytest.fixture
def user():
    return UserModel.objects.create_user(username="test", password="password")

@pytest.fixture
def user2():
    return UserModel.objects.create_user(username="test2", password="password2")

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def logged(client, user):
    client.force_login(user)

@pytest.fixture
def student(user):
    return Student.objects.create(user=user)

@pytest.fixture
def teacher(user2):
    return Teacher.objects.create(user=user2)

@pytest.fixture
def teacher_with_student(teacher, student):
    teacher_with_student = teacher.students.add(student)
    return teacher_with_student