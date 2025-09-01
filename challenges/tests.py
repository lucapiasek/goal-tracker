import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_challenge_list_view(client, user, logged):
    """
    Challenge list view exists and provides correct template
    """
    url = reverse('challenges:list', args=[user.username])
    response = client.get(url)
    assert response.status_code == 200
    template_names = [t.name for t in response.templates if t.name is not None]
    assert 'challenges/challenge_list.html' in template_names
