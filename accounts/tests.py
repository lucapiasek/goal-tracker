from django.test import Client
from .models import Teacher
import pytest
from django.shortcuts import reverse

@pytest.mark.django_db
def test_login_view_post(user):
    c = Client()
    url = reverse('accounts:login')
    response = c.post(url, {'username': 'username', 'password': 'password'})
    assert response.status_code == 200

@pytest.mark.django_db
def test_user_detail_view_has_visible_username(client, user):
    client.force_login(user)
    url = reverse('accounts:user_detail', args=[user.username])
    response = client.get(url)
    assert response.status_code == 200
    assert user.username in response.content.decode('utf-8')

@pytest.mark.django_db
def test_user_detail_view_is_visible_for_his_teacher(client, user2, student):
    teacher = Teacher.objects.create(user=user2)
    teacher.students.add(student)
    client.force_login(user2)
    url = reverse('accounts:user_detail', args=[student.user.username])
    response = client.get(url)
    assert response.status_code == 200
    assert student.user.username in response.content.decode('utf-8')