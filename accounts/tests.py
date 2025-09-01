from django.test import Client
from .models import Teacher, Student
import pytest
from django.shortcuts import reverse
from .forms import InvitationForm

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

@pytest.mark.django_db
def test_student_invite_view_get(client, user, logged):
    """
    Student invite view get method returns invitation form and proper template.
    """
    url = reverse("accounts:invite_teacher")
    response = client.get(url)
    assert response.status_code == 200
    form = response.context['form']
    assert isinstance(form, InvitationForm)

@pytest.mark.django_db
def test_student_invite_view_post(client, user, logged, user2):
    """
    Student invite view post method:
    creates teacher profile for invited user,
    student profile for inviting user,
    then adds teacher profile to students' invitations
    """
    data = {
        'inviting': user.username,
        'invited': user2.username,
        'invitation_type': 'student',
    }
    url = reverse("accounts:invite_teacher")
    response = client.post(url, data)
    assert Student.objects.get(user=user)
    assert Teacher.objects.get(user=user2)
    assert user.student.invitations.all().contains(user2.teacher)
