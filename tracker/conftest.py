import pytest
from django.test import Client
from django.contrib.auth import get_user_model
from .models import Goal, Piece

UserModel = get_user_model()

@pytest.fixture
def user():
    return UserModel.objects.create_user(username="test", password="password")

@pytest.fixture
def user2():
    return UserModel.objects.create_user(username="test2", password="password")

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def goal(user):
    goal = Goal.objects.create(name='Koncert', user=user)
    return goal

@pytest.fixture
def piece(user):
    piece = Piece.objects.create(name='L. van Beethoven - Koncert c-moll', user=user)
    return piece
