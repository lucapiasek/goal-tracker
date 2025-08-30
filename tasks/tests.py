import pytest
from django.urls import reverse
from tracker.models import Goal, Task

@pytest.mark.django_db
def test_task_list_view(client, user, logged):
    """
    Task list view exist and provides correct template.
    """
    url = reverse('tasks:list', args=[user.username])
    response = client.get(url)
    assert response.status_code == 200
    template_names = [t.name for t in response.templates if t.name is not None]
    assert 'tasks/task_list.html' in template_names

@pytest.mark.django_db
def test_task_list_view_with_task(client, user, logged, goal_task):
    """
    Task list view provides existing task.
    """
    url = reverse('tasks:list', args=[user.username])
    response = client.get(url)
    assert response.status_code == 200
    assert goal_task in response.context['task_list']

@pytest.mark.django_db
def test_task_list_view_with_multiple_tasks(client, user, logged, goal_task, piece_task):
    """
    Task list view provides all existing user's tasks.
    """
    url = reverse('tasks:list', args=[user.username])
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['task_list'].count() == 2

@pytest.mark.django_db
def test_task_list_view_provides_user_tasks_only(client, user, logged, user2, goal_task):
    """
    Task list view provides doesn't provide other users' tasks.
    """
    other_user_goal = Goal.objects.create(name="Koncert", user=user2)
    other_user_task = Task.objects.create(goal=other_user_goal, user=user2)
    url = reverse('tasks:list', args=[user.username])
    response = client.get(url)
    assert response.status_code == 200
    assert goal_task in response.context['task_list']
    assert other_user_task not in response.context['task_list']