import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_task_list_view(client, user):
    """
    Task list view exist and provides correct template.
    """
    url = reverse('tasks:list', args=[user.username])
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    template_names = [t.name for t in response.templates if t.name is not None]
    assert 'tasks/task_list.html' in template_names