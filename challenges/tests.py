import pytest
from django.urls import reverse
from tasks.forms import TaskForm
from .forms import ChallengeForm
from tracker.models import Task, Challenge

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

@pytest.mark.django_db
def test_challenge_list_view_with_challenge(client, user, logged, goal_task_challenge):
    """
    Challenge list view provides users' challenge.
    """
    url = reverse('challenges:list', args=[user.username])
    response = client.get(url)
    assert response.status_code == 200
    assert goal_task_challenge in response.context['challenge_list']

@pytest.mark.django_db
def test_challenge_list_view_with_multiple_challenges(client, user, logged, goal_task_challenge, piece_task_challenge):
    """
    Challenge list view provides all users' challenges.
    """
    url = reverse('challenges:list', args=[user.username])
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['challenge_list'].count() == 2

@pytest.mark.django_db
def test_challenge_detail_view(client, user, logged, goal_task_challenge):
    """
    Challenge detail view provides correct template and challenge.
    """
    url = reverse('challenges:detail', args=[user.username, goal_task_challenge.pk])
    response = client.get(url)
    assert response.status_code == 200
    assert goal_task_challenge == response.context['challenge']
    template_names = [t.name for t in response.templates if t.name is not None]
    assert 'challenges/challenge_detail.html' in template_names

@pytest.mark.django_db
def test_challenge_detail_view_with_non_existent_challenge(client, user, logged, goal_task_challenge):
    """
    Challenge detail view return 404 when requested challenge doesn't exist.
    """
    url = reverse('challenges:detail', args=[user.username, goal_task_challenge.pk + 1])
    response = client.get(url)
    assert response.status_code == 404

@pytest.mark.django_db
def test_challenge_create_view_get(client, user, logged):
    """
    Challenge create view provides task form and challenge form.
    """
    url = reverse('challenges:create', args=[user.username])
    response = client.get(url)
    assert response.status_code == 200
    for form in response.context['forms']:
        assert isinstance(form, TaskForm) or isinstance(form, ChallengeForm)

@pytest.mark.django_db
def test_challenge_create_view_post(client, user, logged, goal):
    """
    Challenge create view creates task and related to it challenge.
    """
    url = reverse('challenges:create', args=[user.username])
    data = {
        'goal': goal.id,
        'minimum_number_of_days': 0,
        'minimum_number_of_repetitions': 0,
        'minimum_total_repetitions': 0
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert Task.objects.get(user=user, goal=goal)
    task = Task.objects.get(user=user, goal=goal)
    assert Challenge.objects.get(task=task)

@pytest.mark.django_db
def test_challenge_delete_view_get(client, user, logged, goal_task_challenge):
    """
    Challenge delete view get method provides correct template and task.
    """
    url = reverse('challenges:delete', args=[user.username, goal_task_challenge.pk])
    response = client.get(url)
    assert response.status_code == 200
    template_names = [t.name for t in response.templates if t.name is not None]
    assert 'challenges/delete_form.html' in template_names
    assert goal_task_challenge == response.context['object_to_delete']

@pytest.mark.django_db
def test_challenge_delete_view_post(client, user, logged, goal_task_challenge):
    """
    Challenge delete view post method removes challenge from database.
    """
    url = reverse('challenges:delete', args=[user.username, goal_task_challenge.pk])
    operation = {'operation': 'Tak'}
    response = client.post(url, operation)
    assert not Challenge.objects.all().contains(goal_task_challenge)
