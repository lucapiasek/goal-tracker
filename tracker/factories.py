import factory
from tracker.models import Goal, Piece

class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goal

    name = factory.Faker('sentence')

class PieceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Piece

    name = factory.Faker('name')