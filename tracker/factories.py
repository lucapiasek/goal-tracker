import factory
from tracker.models import Goal

class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goal

    name = factory.Faker('sentence')