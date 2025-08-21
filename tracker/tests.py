from django.urls import reverse
import pytest
from pytest_django.asserts import assertTemplateUsed
from tracker.models import Goal
from tracker.factories import GoalFactory, PieceFactory
from tracker.forms import GoalCreateForm
import datetime


@pytest.mark.django_db
def test_goal_list_view_with_no_goals(client):
    """
    Goals view exists and provides correct template.
    """
    url = reverse('tracker:goal_list')
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, 'tracker/goal_list.html')

@pytest.mark.django_db
def test_goal_list_view_with_one_full_goal(client, goal):
    goal.date = datetime.date(year=2025, month=12, day=31)
    goal.time = datetime.time(hour=23, minute=59, second=59)
    goal.additional_info = 'Additional information'
    goal.save()
    url = reverse('tracker:goal_list')
    response = client.get(url)
    assert response.status_code == 200
    assert "Dec. 31, 2025" in response.content.decode('utf-8')
    assert response.context['goal_list'].count() == 1

@pytest.mark.django_db
def test_goal_list_view_with_multiple_goals(client):
    goal1 = GoalFactory()
    goal2 = GoalFactory()
    url = reverse('tracker:goal_list')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['goal_list'].count() == 2

@pytest.mark.django_db
def test_goal_detail_view_returns_404_with_non_existent_goal(client):
    url = reverse('tracker:goal_detail', args=[1])
    response = client.get(url)
    assert response.status_code == 404

@pytest.mark.django_db
def test_goal_detail_view(client, goal):
    url = reverse('tracker:goal_detail', args=[goal.pk])
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, 'tracker/goal_detail.html')
    assert goal.pk == response.context['goal'].pk

@pytest.mark.django_db
def test_goal_create_view_get(client):
    url = reverse('tracker:goal_create')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context["form"], GoalCreateForm)

@pytest.mark.django_db
def test_goal_create_view_post(client):
    url = reverse('tracker:goal_create')
    goal_data = {
        'name': "Koncert"
    }
    response = client.post(url, goal_data)
    assert response.status_code == 302
    assert Goal.objects.get(**goal_data)

@pytest.mark.django_db
def test_pieces_view_with_no_pieces(client):
    url = reverse('tracker:pieces')
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, 'tracker/piece_list.html')

@pytest.mark.django_db
def test_pieces_view_with_multiple_pieces(client):
    piece1 = PieceFactory()
    piece2 = PieceFactory()
    url = reverse('tracker:pieces')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['piece_list'].count() == 2

@pytest.mark.django_db
def test_pieces_view_with_full_piece(client, piece):
    piece.composer = 'J.S.Bach'
    piece.opus = 'BWV 266'
    piece.number = '1a'
    piece.is_cleared = True
    piece.is_mastered = True
    piece.save()
    url = reverse('tracker:pieces')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['piece_list'].count() == 1
    assert "Utwór opanowany" in response.content.decode('utf-8')