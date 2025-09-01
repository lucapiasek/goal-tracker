import pytest
from django.test import Client
from django.contrib.auth import get_user_model
from tracker.models import Task, Practice, Goal, Piece, Challenge
from factory import Faker

UserModel = get_user_model()

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def user():
    return UserModel.objects.create_user(username="test", password="password")

@pytest.fixture
def logged(client, user):
    client.force_login(user)

@pytest.fixture
def user2():
    return UserModel.objects.create_user(username="test2", password="password")

@pytest.fixture
def goal(user):
    return Goal.objects.create(user=user, name=Faker("sentence"))

@pytest.fixture
def piece(user):
    return Piece.objects.create(user=user, name_to_display=Faker("name"))

@pytest.fixture
def goal_task(user, goal):
    return Task.objects.create(user=user, goal=goal)

@pytest.fixture
def piece_task(user, piece):
    return Task.objects.create(user=user, piece=piece)

@pytest.fixture
def goal_task_challenge(user, goal_task):
    return Challenge.objects.create(user=user, task=goal_task)

@pytest.fixture
def piece_task_challenge(user, piece_task):
    return Challenge.objects.create(user=user, task=piece_task)
