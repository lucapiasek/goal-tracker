from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_not_required, login_required
from django.contrib.auth import get_user_model, logout, get_user
from django.utils import timezone
from django.utils.decorators import method_decorator
from .models import Teacher, Student
from django.forms import modelform_factory
from .permissions import is_owner_or_is_teacher

UserModel = get_user_model()

@method_decorator(login_not_required, name='dispatch')
class UserCreateView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'accounts/create_user.html', {'form': form, 'page_title': "Zarejestruj się"})

    def post(self, request):
        form = UserCreationForm(request.POST)
        user = form.save()
        return redirect('tracker_calendar:year', user.username, timezone.now().year)

class LoginView(LoginView):
    template_name = 'accounts/login_form.html'
    next_page = 'accounts:user_update'
    extra_context = {'page_title': "Zaloguj się"}
    redirect_authenticated_user = True

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
        return is_owner_or_is_teacher(self.request, self.kwargs['username'])

    def get(self, request, username):
        owner = get_object_or_404(UserModel, username=username)

        if not hasattr(owner, 'teacher'):
            owner.teacher = False
        else:
            owner = UserModel.objects.select_related('teacher').get(id=owner.id)

        if not hasattr(owner, 'student'):
            owner.student = False
        else:
            owner = UserModel.objects.select_related('student').get(id=owner.id)
        return render(request, 'accounts/user_detail.html', {'owner': owner})

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
