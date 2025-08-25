import factory
from tracker.models import Goal, Piece
from django.contrib.auth import get_user_model

UserModel = get_user_model

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserModel

    username =  factory.Faker('word')
    password = factory.Faker('password')

class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goal

    name = factory.Faker('sentence')

class PieceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Piece

    name = factory.Faker('name')