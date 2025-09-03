import pytest
from django.urls import reverse
from tracker.models import Goal, Task, Practice
from accounts.models import Teacher, Student
from .forms import TaskForm, PracticeForm


@pytest.mark.django_db
def test_task_list_view(client, user, logged):
    """
    Task list view exists and provides correct template.
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

@pytest.mark.django_db
def test_task_list_view_is_forbidden_for_other_user(client, user, user2, goal_task):
    """
    User's task list view is forbidden for other users
    """
    client.force_login(user2)
    url = reverse('tasks:list', args=[user.username])
    response = client.get(url)
    assert response.status_code == 403

@pytest.mark.django_db
def test_task_list_view_is_allowed_for_teacher(client, user, user2, goal_task):
    """
    User's task list view provides user's tasks for their teacher
    """
    teacher, created = Teacher.objects.get_or_create(user=user2)
    student, create = Student.objects.get_or_create(user=user)
    teacher.students.add(student)
    client.force_login(teacher.user)
    url = reverse('tasks:list', args=[student.user.username])
    response = client.get(url)
    assert response.status_code == 200
    assert goal_task in response.context['task_list']

@pytest.mark.django_db
def test_task_detail_view(client, goal_task, user, logged):
    """
    Task detail view provides correct template and users' task.
    """
    url = reverse('tasks:detail', args=[user.username, goal_task.pk])
    response = client.get(url)
    assert response.status_code == 200
    assert goal_task == response.context['task']
    template_names = [t.name for t in response.templates if t.name is not None]
    assert 'tasks/task_detail.html' in template_names

@pytest.mark.django_db
def test_task_detail_view_with_non_existent_goal(client, user, logged):
    """
    Task detail view return 404 when requested goal doesn't exist.
    """
    url = reverse('tasks:detail', args=[user.username, 1])
    response = client.get(url)
    assert response.status_code == 404

@pytest.mark.django_db
def test_task_detail_view_with_practice_set(client, user, logged, goal_task, goal_task_practice):
    """
    Task detail view provides all practice instances of task.
    """
    goal_task_practice_2 = Practice.objects.create(task=goal_task, date='2025-09-12')
    url = reverse('tasks:detail', args=[user.username, goal_task.pk])
    response = client.get(url)
    assert response.status_code == 200
    assert str(goal_task_practice) in response.content.decode('utf-8')
    assert str(goal_task_practice_2) in response.content.decode('utf-8')

@pytest.mark.django_db
def test_task_create_view_get(client, user, logged):
    """
    Task create view provides task form and practice form.
    """
    url = reverse('tasks:create', args=[user.username])
    response = client.get(url)
    assert response.status_code == 200;
    for form in response.context['forms']:
        assert isinstance(form, TaskForm) or isinstance(form, PracticeForm)
