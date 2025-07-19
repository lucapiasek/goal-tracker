import pytest
from django.test import Client
from tracker.factories import GoalFactory

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def goal():
    return GoalFactory()
