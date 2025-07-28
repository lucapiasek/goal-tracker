from django.urls import reverse
import pytest
from pytest_django.asserts import assertTemplateUsed
from tracker.models import Goal
from tracker.factories import GoalFactory, PieceFactory
from django.core.exceptions import ValidationError
import datetime


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

@pytest.mark.django_db
def test_goals_view_with_one_full_goal(client, goal):
    goal.date = datetime.date(year=2025, month=12, day=31)
    goal.time = datetime.time(hour=23, minute=59, second=59)
    goal.additional_info = 'Additional information'
    goal.save()
    url = reverse('tracker:goals')
    response = client.get(url)
    assert response.status_code == 200
    assert "Dec. 31, 2025" in response.content.decode('utf-8')
    assert response.context['goal_list'].count() == 1

@pytest.mark.django_db
def test_goals_view_with_multiple_goals(client):
    goal1 = GoalFactory()
    goal2 = GoalFactory()
    url = reverse('tracker:goals')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['goal_list'].count() == 2

@pytest.mark.django_db
def test_goal_view_returns_404_with_non_existent_goal(client):
    url = reverse('tracker:goal', args=[1])
    response = client.get(url)
    assert response.status_code == 404

@pytest.mark.django_db
def test_goal_detail_view(client, goal):
    url = reverse('tracker:goal', args=[goal.pk])
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, 'tracker/goal.html')
    assert goal.pk == response.context['goal'].pk


@pytest.mark.django_db
def test_pieces_view_with_no_pieces(client):
    url = reverse('tracker:pieces')
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, 'tracker/pieces.html')

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