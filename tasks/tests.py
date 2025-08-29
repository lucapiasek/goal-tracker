import pytest
from django.test import Client
from django.contrib.auth import get_user_model
from tracker.models import Task, Practice

UserModel = get_user_model()

@pytest.fixture
def user():
    return UserModel.objects.create_user(username="test2", password="password")

@pytest.fixture
def user2():
    return UserModel.objects.create_user(username="test2", password="password")

