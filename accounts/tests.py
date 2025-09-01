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
def test_student_invite_view_post(client, user, logged, student, teacher):
    """
    Student invite view adds teacher profile to students' invitations.
    """
    url = reverse('accounts:invite_teacher')
    data = {
        'inviting': student.user.username,
        'invited': teacher.user.username,
        'invitation_type': 'student'
    }
    response = client.post(url, data)
    assert student.invitations.all().contains(teacher)

@pytest.mark.django_db
def test_student_invite_view_post_creates_profiles(client, user, logged, user2):
    """
    Student invite view post method creates profiles if they don't exist:
    teacher profile for invited user,
    student profile for inviting user,
    then adds teacher to student invitations.
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
    student = Student.objects.get(user=user)
    assert student.invitations.all().contains(user2.teacher)

@pytest.mark.django_db
def test_teacher_invite_view_post(client, user, user2, student, teacher):
    """
    Teacher invite view adds student profile to teacher invitations.
    """
    client.force_login(user2)
    data = {
        'inviting': user2.username,
        'invited': user.username,
        'invitation_type': 'teacher'
    }
    url = reverse('accounts:invite_student')
    client.post(url, data)
    assert teacher.invitations.all().contains(student)

@pytest.mark.django_db
def test_teacher_invite_view_post_creates_profiles(client, user, logged, user2):
    """
    Teacher invite view post method creates profiles if they don't exist:
    teacher profile for inviting user,
    student profile for invited user,
    then adds student to teacher invitations.
    """
    url = reverse('accounts:invite_student')
    data = {
        'inviting': user.username,
        'invited': user2.username,
        'invitation_type': 'teacher'
    }
    response = client.post(url, data)
    assert Teacher.objects.get(user=user)
    assert Student.objects.get(user=user2)
    teacher = Teacher.objects.get(user=user)
    assert teacher.invitations.all().contains(user2.student)