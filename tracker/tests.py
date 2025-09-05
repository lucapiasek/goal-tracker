from django.urls import reverse
import pytest
from pytest_django.asserts import assertTemplateUsed
from tracker.models import Goal, Piece
from tracker.forms import GoalCreateForm, GoalUpdateForm
import datetime
from django.contrib.auth import get_user_model

UserModel = get_user_model()

@pytest.mark.django_db
def test_goal_list_view_with_no_goals(client, user):
    """
    Goals view exists and provides correct template.
    """
    url = reverse('tracker:goal_list', args=[user.username])
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    template_names = [t.name for t in response.templates if t.name is not None]
    assert 'tracker/goal_list.html' in template_names

@pytest.mark.django_db
def test_foreign_user_is_forbidden_from_other_users_goals(client, user):
    """
    Goal list view is forbidden for non-logged user visit.
    """
    user2 = UserModel.objects.create_user(username="test2", password='password')
    client.force_login(user)
    url = reverse('tracker:goal_list', args=[user2.username])
    response = client.get(url)
    assert response.status_code == 403

@pytest.mark.django_db
def test_goal_list_view_with_one_full_goal(client, goal, user):
    """
    Goal list view has visible existing goal.
    """
    client.force_login(user)
    goal.date = datetime.date(year=2025, month=12, day=31)
    goal.time = datetime.time(hour=23, minute=59, second=59)
    goal.additional_info = 'Additional information'
    goal.save()
    url = reverse('tracker:goal_list', args=[user.username])
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['goal_list'].count() == 1

@pytest.mark.django_db
def test_goal_list_view_with_multiple_goals(client, user, goal):
    """
    Goal list view provides all user goals.
    """
    goal2 = Goal.objects.create(user=user, name="Audycja")
    client.force_login(user)
    url = reverse('tracker:goal_list', args=[user.username])
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['goal_list'].count() == 2

@pytest.mark.django_db
def test_goal_list_view_provides_only_user_goals(client, user, user2, goal):
    """
    Goal list view provides all user goals.
    """
    goal2 = Goal.objects.create(user=user, name="Audycja")
    goal3 = Goal.objects.create(user=user2, name="Audycja")
    client.force_login(user)
    url = reverse('tracker:goal_list', args=[user.username])
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['goal_list'].count() == 2

@pytest.mark.django_db
def test_goal_detail_view_returns_404_with_non_existent_goal(client, user):
    """
    Goal list view raises 404 when goal doesn't exist.
    """
    client.force_login(user)
    url = reverse('tracker:goal_detail', args=[user.username, 1])
    response = client.get(url)
    assert response.status_code == 404

@pytest.mark.django_db
def test_goal_detail_view(client, goal, user):
    """
    Goal detail view provides correct template and goal for logged user
    """
    client.force_login(user)
    url = reverse('tracker:goal_detail', args=[user.username, goal.pk])
    response = client.get(url)
    assert response.status_code == 200
    template_names = [t.name for t in response.templates if t.name is not None]
    assert 'tracker/goal_detail.html' in template_names
    assert goal.pk == response.context['goal'].pk

@pytest.mark.django_db
def test_goal_create_view_get(client, user):
    client.force_login(user)
    url = reverse('tracker:goal_create', args=[user.username])
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context["form"], GoalCreateForm)

@pytest.mark.django_db
def test_goal_create_view_post(client, user):
    client.force_login(user)
    url = reverse('tracker:goal_create', args=[user.username])
    goal_data = {
        'name': "Koncert"
    }
    response = client.post(url, goal_data)
    assert response.status_code == 302
    assert Goal.objects.get(**goal_data)

@pytest.mark.django_db
def test_goal_update_view_get(client, user, goal):
    """
    Goal update view get method returns form with goal as an instance
    """
    client.force_login(user)
    url = reverse('tracker:goal_update', args=[user.username, goal.pk])
    response = client.get(url)
    assert response.status_code == 200
    form = response.context['form']
    assert isinstance(form, GoalUpdateForm)
    assert form.instance == goal

@pytest.mark.django_db
def test_goal_update_view_post(client, user, goal):
    """
    Goal update view post method saves changes in goal to database.
    """
    client.force_login(user)
    url = reverse('tracker:goal_update', args=[user.username, goal.pk])
    data = {'name': goal.name, 'additional_info': 'test_info_update'}
    response = client.post(url, data)
    assert response.status_code == 302
    assert Goal.objects.get(pk=goal.pk, **data)

@pytest.mark.django_db
def test_pieces_view_with_no_pieces(client, piece, user):
    client.force_login(user)
    url = reverse('tracker:piece_list', args=[user.username])
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, 'tracker/piece_list.html')

@pytest.mark.django_db
def test_pieces_view_with_multiple_pieces(client, piece, user):
    client.force_login(user)
    piece2 = Piece.objects.create(user=user, name_to_display="Fantazja c-moll")
    url = reverse('tracker:piece_list', args=[user.username])
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['piece_list'].count() == 2

@pytest.mark.django_db
def test_pieces_view_with_full_piece(client, piece, user):
    client.force_login(user)
    piece.composer = 'J.S.Bach'
    piece.opus = 'BWV 266'
    piece.number = '1a'
    piece.is_cleared = True
    piece.is_mastered = True
    piece.save()
    url = reverse('tracker:piece_list', args=[user.username])
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['piece_list'].count() == 1
    assert "Utwór opanowany" in response.content.decode('utf-8')