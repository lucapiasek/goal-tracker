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
    Task detail view provides correct template and user's task.
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

@pytest.mark.django_db
def test_task_create_view_post(client, user, logged, goal):
    """
    Task create view creates task and related to it practice.
    """
    url = reverse('tasks:create', args=[user.username])
    data = {
        'user': user,
        'goal': goal.id,
        'date': '12.09.2025'
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert Task.objects.get(user=user, goal=goal)
    task = Task.objects.get(user=user, goal=goal)
    assert Practice.objects.get(task=task, date='2025-09-12')

@pytest.mark.django_db
def test_task_update_view_get(client, user, logged, goal_task):
    """
    Task update view provides correct form and task instance.
    """
    url = reverse('tasks:update', args=[user.username, goal_task.pk])
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], TaskForm)
    assert response.context['form'].instance == goal_task
    template_names = [t.name for t in response.templates if t.name is not None]
    assert 'tasks/create_form.html' in template_names

@pytest.mark.django_db
def test_task_update_view_post(client, user, logged, goal, goal_task):
    """
    Task update view post method saves changes in task.
    """
    url = reverse('tasks:update', args=[user.username, goal_task.pk])
    data = {'goal': goal.pk, 'method': 'Calmly'}
    response = client.post(url, data)
    assert response.status_code == 302
    assert Task.objects.get(pk=goal_task.pk, method=data['method'])

@pytest.mark.django_db
def test_task_delete_view_get(client, user, logged, goal_task):
    """
    Task delete view provides correct template.
    """
    url = reverse('tasks:delete', args=[user.username, goal_task.pk])
    response = client.get(url)
    assert response.status_code == 200
    template_names = [t.name for t in response.templates if t.name is not None]
    assert 'tasks/delete_form.html' in template_names

@pytest.mark.django_db
def test_task_delete_view_post(client, user, logged, goal_task):
    """
    Task delete view removes task from database.
    """
    url = reverse('tasks:delete', args=[user.username, goal_task.pk])
    data = {'operation': 'Tak'}
    response = client.post(url, data)
    assert response.status_code == 302
    assert not Task.objects.all().contains(goal_task)

@pytest.mark.django_db
def test_task_delete_view_post_removes_practices(client, user, logged, goal_task, goal_task_practice):
    """
    Task delete view removes practice set related to task.
    """
    url = reverse('tasks:delete', args=[user.username, goal_task.pk])
    data = {'operation': 'Tak'}
    response = client.post(url, data)
    assert not Practice.objects.all().contains(goal_task_practice)

@pytest.mark.django_db
def test_practice_create_view_get(client, user, logged, goal_task):
    """
    Practice create view get method provides correct form.
    """
    url = reverse('tasks:practice_create', args=[user.username, goal_task.pk])
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], PracticeForm)

@pytest.mark.django_db
def test_practice_create_view_post(client, user, logged, goal_task):
    """
    Practice create view post method creates practice for task.
    """
    url = reverse('tasks:practice_create', args=[user.username, goal_task.pk])
    data = {
        'date': '2025-12-09'
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert Practice.objects.get(task=goal_task.pk, **data)

@pytest.mark.django_db
def test_practice_create_view_get_returns_404_with_non_existent_task(client, user, logged, goal_task):
    """
    Practice create view get method returns 404 when task doesn't exist.
    """
    url = reverse('tasks:practice_create', args=[user.username, goal_task.pk + 1])
    response = client.get(url)
    assert response.status_code == 404

@pytest.mark.django_db
def test_practice_create_view_post_returns_404_with_non_existent_task(client, user, logged, goal_task):
    """
    Practice create view post method returns 404 when task doesn't exist.
    """
    url = reverse('tasks:practice_create', args=[user.username, goal_task.pk + 1])
    response = client.post(url)
    assert response.status_code == 404

@pytest.mark.django_db
def test_practice_create_view_is_forbidden_for_teacher(client, user, student, user2, teacher, teacher_has_student, goal_task):
    """
    Practice create view get method returns 403 for user's teacher.
    """
    client.force_login(user2)
    url = reverse('tasks:practice_create', args=[user.username, goal_task.pk])
    response = client.get(url)
    assert response.status_code == 403
    response = client.post(url)
    assert response.status_code == 403

@pytest.mark.django_db
def test_practice_update_view_get(client, user, logged, goal_task, goal_task_practice):
    """
    Practice update view get method return form with correct practice.
    """
    url = reverse('tasks:practice_update', args=[user.username, goal_task_practice.pk])
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['form'].instance == goal_task_practice

@pytest.mark.django_db
def test_practice_update_view_post(client, user, logged, goal_task, goal_task_practice):
    """
    Practice update view post method updates practice data in database.
    """
    url = reverse('tasks:practice_update', args=[user.username, goal_task_practice.pk])
    data = {
        'date': '2009-09-09',
        'repetitions': 9
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert Practice.objects.get(pk=goal_task_practice.pk, **data)

@pytest.mark.django_db
def test_practice_update_view_returns_404_with_non_existent_practice(client, user, logged, goal_task, goal_task_practice):
    """
    Practice update view return 404 when practice doesn't exist.
    """
    url = reverse('tasks:practice_update', args=[user.username, goal_task_practice.pk + 1])
    response = client.get(url)
    assert response.status_code == 404
    response = client.post(url)
    assert response.status_code == 404

@pytest.mark.django_db
def test_practice_update_view_is_forbidden_for_teacher(client, user, student, user2, teacher, teacher_has_student, goal_task_practice):
    """
    Practice update view is forbidden for user's teacher.
    """
    client.force_login(user2)
    url = reverse('tasks:practice_update', args=[user.username, goal_task_practice.pk])
    response = client.get(url)
    assert response.status_code == 403
    response.client.post(url)
    assert response.status_code == 403

@pytest.mark.django_db
def test_practice_delete_view_get(client, user, logged, goal_task_practice):
    """
    Practice delete view provides correct template.
    """
    url = reverse('tasks:practice_delete', args=[user.username, goal_task_practice.pk])
    response = client.get(url)
    assert response.status_code == 200
    template_names = [t.name for t in response.templates if t.name is not None]
    assert 'tasks/delete_form.html' in template_names

@pytest.mark.django_db
def test_practice_delete_view_post(client, user, logged, goal_task_practice):
    """
    Practice delete view deletes practice from database.
    """
    url = reverse('tasks:practice_delete', args=[user.username, goal_task_practice.pk])
    operation = {'operation': 'Tak'}
    response = client.post(url, operation)
    assert not Practice.objects.all().contains(goal_task_practice)
