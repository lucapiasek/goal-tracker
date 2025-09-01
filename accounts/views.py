from django.http import Http404
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_not_required
from django.contrib.auth import get_user_model, login, logout, get_user
from django.utils import timezone
from django.utils.decorators import method_decorator
from .forms import InvitationForm
from .models import Teacher, Student
from django.forms import modelform_factory
from .permissions import is_owner_or_is_teacher, is_owner
from .utils import if_not_teacher_create, if_not_student_create

UserModel = get_user_model()


class UserCreateView(View):
    @method_decorator(login_not_required)
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'accounts/create_user.html', {'form': form, 'page_title': "Zarejestruj się"})

    @method_decorator(login_not_required)
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            year = timezone.now().year
            return redirect('tracker_calendar:year', user.username, year)
        return render(request, 'accounts/create_user.html', {'form': form, 'page_title': "Zarejestruj się"})

class LoginView(LoginView):
    template_name = 'accounts/login_form.html'
    next_page = 'accounts:user_update'
    extra_context = {'page_title': "Zaloguj się"}
    redirect_authenticated_user = False

    def get_default_redirect_url(self):
        return reverse('accounts:user_detail', args=[self.request.user.username])

class LogoutView(View):
    def get(self, request):
        return render(
            request,
            'accounts/confirmation_form.html',
            {'question':  "Czy na pewno chcesz się wylogować?"})

    def post(self, request):
        logout(request)
        return redirect('accounts:login')

class UserDetailView(UserPassesTestMixin, View):
    def test_func(self):
        return is_owner_or_is_teacher(self.request.user, self.kwargs['username'])

    def get(self, request, username):
        owner = get_object_or_404(UserModel, username=username)

        if not hasattr(owner, 'teacher'):
            is_teacher = False
        else:
            owner = UserModel.objects.select_related('teacher').get(id=owner.id)
            is_teacher = True

        if not hasattr(owner, 'student'):
            is_student = False
        else:
            owner = UserModel.objects.select_related('student').get(id=owner.id)
            is_student = True
        return render(request, 'accounts/user_detail.html', {'owner': owner, 'is_teacher': 'is_teacher', 'is_student': 'is_student'})

class UserUpdateView(View):
    def get(self, request):
        owner = get_user(request)
        UserForm = modelform_factory(
            UserModel,
            fields=['first_name', 'last_name', 'email'],
            labels={'first_name': 'Imię', 'last_name': 'Nazwisko'}
        )
        form = UserForm(instance=owner)
        return render(request, 'accounts/create_form.html', {'form': form, 'owner': owner})

    def post(self, request):
        owner = get_user(request)
        UserForm = modelform_factory(
            UserModel,
            fields=['first_name', 'last_name', 'email'],
            labels={'first_name': 'Imię', 'last_name': 'Nazwisko'}
            )
        form = UserForm(request.POST, instance=owner)
        user = form.save()
        return redirect('accounts:user_detail', user.username)

class StudentInviteView(View):
    def get(self, request):
        form = InvitationForm(initial={
            'inviting': request.user.username,
            'invitation_type': 'student'
        })
        return render(request, 'accounts/search_form.html', {
            'form': form,
            'page_title': 'Zaproś nauczyciela',
            'button_value': 'Zaproś',
            'owner': request.user
        })

    def post(self, request):
        form = InvitationForm(request.POST, initial={
            'inviting': request.user.username,
            'invitation_type': 'student'
        })
        if form.is_valid():
            invited_username = form.cleaned_data.get('invited')
            invited_user = UserModel.objects.get(username=invited_username)
            invited_teacher, created = Teacher.objects.get_or_create(user=invited_user)
            inviting_user = get_user(request)
            inviting_student, created = Student.objects.get_or_create(user=inviting_user)
            inviting_student.invitations.add(invited_teacher)
            return render(request, 'accounts/success.html', {
                'page_title': 'Zaproś nauczyciela',
                'success_message': 'Nauczyciel został zaproszony.',
                'owner': inviting_user
            })
        return render(request, 'accounts/search_form.html', {
            'form': form,
            'page_title': 'Zaproś nauczyciela',
            'button_value': 'Zaproś',
            'owner': request.user
        })

class TeacherInviteView(View):
    def get(self, request):
        form = InvitationForm(initial={
            'inviting': request.user.username,
            'invitation_type': 'teacher'
        })
        return render(request, 'accounts/search_form.html', {
            'form': form,
            'page_title': 'Zaproś Ucznia',
            'button_value': 'Zaproś',
            'owner': request.user
        })

    def post(self, request):
        form = InvitationForm(request.POST, initial={
            'inviting': request.user.username,
            'invitation_type': 'teacher'
        })
        if form.is_valid():
            invited_username = form.cleaned_data.get('invited')
            invited_user = UserModel.objects.get(username=invited_username)
            invited_student, created = Student.objects.get_or_create(user=invited_user)
            inviting_user = get_user(request)
            inviting_teacher, created = Teacher.ojbects.get_or_create(user=inviting_user)
            inviting_teacher.invitations.add(invited_student)
            return render(request, 'accounts/success.html', {
                'page_title': 'Zaproś nauczyciela',
                'success_message': "Student został zaproszony.",
                'owner': inviting_user
            })
        return render(request, 'accounts/search_form.html', {
            'form': form,
            'page_title': 'Zaproś Ucznia',
            'button_value': 'Zaproś',
            'owner': request.user
        })

class AcceptStudentInvitationView(View):
    def get(self, request, username):
        inviting_user = get_object_or_404(UserModel, username=username)
        invited_user = get_user(request)
        if hasattr(inviting_user, 'student') and hasattr(invited_user, 'teacher'):
            if invited_user.teacher.student_invitations.contains(inviting_user.student):
                return render(request, 'accounts/confirmation_form.html', {
                    'question': f"Czy chcesz potwierdzić zaproszenie od studenta {inviting_user.username}",
                    'owner': request.user
                })
        raise Http404("Page not found.")

    def post(self, request, username):
        invited_user = get_user(request)
        operation = request.POST['operation']
        if operation == 'Tak':
            inviting_user = get_object_or_404(UserModel, username=username)
            invited_user.teacher.students.add(inviting_user.student)
            invited_user.save()
            invited_user.teacher.remove_invitations(inviting_user.student)
            success_message = f"Przyjęto zaproszenie od użytkownika {username}"
        if operation == 'Nie':
            inviting_user = get_object_or_404(UserModel, username=username)
            invited_user.remove_invitations(inviting_user.student)
            success_message = "Zaproszenie zostało odrzucone."

        return render(request, 'accounts/success.html', {
            'success_message': success_message,
            'owner': request.user
        })

class AcceptTeacherInvitationView(View):
    def get(self, request, username):
        inviting_user = get_object_or_404(UserModel, username=username)
        invited_user = get_user(request)
        if hasattr(inviting_user, 'teacher') and hasattr(invited_user, 'student'):
            if invited_user.student.teacher_invitations.contains(inviting_user.teacher):
                return render(request, 'accounts/confirmation_form.html', {
                    'question': f"Czy chcesz potwierdzić zaproszenie od studenta {inviting_user.username}",
                    'owner': request.user
                })
        raise Http404("Page not found.")

    def post(self, request, username):
        invited_user = get_user(request)
        if request.POST['operation'] == 'Tak':
            inviting_user = get_object_or_404(UserModel, username=username)
            invited_user.student.teachers.add(inviting_user.teacher)
            invited_user.save()
            invited_user.student.remove_invitations(inviting_user.teacher)
            success_message = f"Przyjęto zaproszenie od użytkownika {username}"
        elif request.POST['operation'] == 'Nie':
            inviting_user = get_object_or_404(UserModel, username=username)
            invited_user.remove_invitations(inviting_user.teacher)
            success_message = "Zaproszenie zostało odrzucone."

        return render(request, 'accounts/success.html', {
            'success_message': success_message,
            'owner': request.user
        })

class InvitationListView(View):
    def get(self, request):
        user = get_user(request)
        teacher_invitations = user.student.teacher_invitations.all() if hasattr(user, 'student') else UserModel.objects.none()
        student_invitations = user.teacher.student_invitations.all() if hasattr(user, 'teacher') else UserModel.objects.none()
        return render(
            request,
            'accounts/invitation_list.html',
            {
                'teacher_invitations': teacher_invitations,
                'student_invitations': student_invitations,
                'owner': request.user
            }
        )
