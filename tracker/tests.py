from django.urls import reverse
import pytest
from pytest_django.asserts import assertTemplateUsed
from tracker.models import Goal
from django.core.exceptions import ValidationError


def test_goal_model_with_all_fields_empty_raises_validation_error():
    goal = Goal()

    with pytest.raises(ValidationError) as exception:
        goal.full_clean()

    assert "At least one of the fields must be filled." in str(exception.value)

@pytest.mark.django_db
def test_goals_view_with_no_goals(client):
    """
    Goals view exists and provides correct template.
    """
    url = reverse('tracker:goals')
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, 'tracker/goals.html')