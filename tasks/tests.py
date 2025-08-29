import pytest
from django.test import Client
from django.contrib.auth import get_user_model
from tracker.models import Task, Practice, Goal, Piece
from factory import Faker

UserModel = get_user_model()

@pytest.fixture
def user():
    return UserModel.objects.create_user(username="test2", password="password")

@pytest.fixture
def user2():
    return UserModel.objects.create_user(username="test2", password="password")

@pytest.fixture
def goal(user):
    return UserModel.objects.create(user=user, name=Faker("sentence"))

@pytest.fixture
def piece(user):
    return UserModel.objects.create(user=user, name_to_display=Faker("name"))

@pytest.fixture
def task_with_goal(user, goal):
    return Task.objects.create(user=user, goal=goal)

@pytest.fixture
def task_with_piece(user, piece):
    return Task.objects.create(user=user, piece=piece)
