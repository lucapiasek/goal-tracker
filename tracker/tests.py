from django.urls import reverse
import pytest
from pytest_django.asserts import assertTemplateUsed

@pytest.mark.django_db
def test_goals_view_with_no_goals(client):
    """
    Goals view exists and provides correct template.
    """
    url = reverse('tracker.goals')
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, 'tracker/goals.html')

