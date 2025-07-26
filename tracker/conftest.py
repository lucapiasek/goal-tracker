import pytest
from django.test import Client
from tracker.factories import GoalFactory, PieceFactory
from pytest_factoryboy import register

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def goal():
    return GoalFactory()

register(PieceFactory)
