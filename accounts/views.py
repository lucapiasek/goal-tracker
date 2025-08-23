from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model, logout, get_user
from django.utils import timezone
from .models import Teacher, Student
from django.forms import modelform_factory

UserModel = get_user_model()

class UserCreateView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'accounts/create_user.html', {'form': form, 'page_title': "Zarejestruj się"})

    def post(self, request):
        form = UserCreationForm(request.POST)
        user = form.save()
        return redirect('tracker_calendar:year', user.username, timezone.now().year)

class LoginView(LoginView):
    template_name = 'accounts/create_user.html'
    next_page = 'accounts:user_update'
    extra_context = {'page_title': "Zaloguj się"}

class LogoutView(View):
    def get(self, request):
        return render(request, 'accounts/logout_form.html')

    def post(self, request):
        logout(request)
        return redirect('accounts:login')

class UserDetailView(View):
    def get(self, request, username):
        owner = get_object_or_404(UserModel, username=username)
        if not hasattr(owner, 'teacher'):
            teacher = Teacher(user=owner)
            teacher.save()
            owner.teacher = teacher
            owner.save()
        owner = UserModel.objects.select_related('teacher').get(id=owner.id)
        if not hasattr(owner, 'student'):
            student = Student(user=owner)
            student.save()
            owner.student = student
            owner.save()
        owner = UserModel.objects.select_related('student').get(id=owner.id)
        return render(request, 'accounts/user_detail.html', {'owner': owner})

class UserUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        owner = get_user(request)
        UserForm = modelform_factory(
            UserModel,
            fields=['first_name', 'last_name', 'email'],
            labels={'first_name': 'Imię', 'last_name': 'Nazwisko'}
        )
        form = UserForm(instance=request.user)
        return render(request, 'accounts/create_form.html', {'form': form, 'owner': owner})

    def post(self, request):
        owner = get_user(request)
        UserForm = modelform_factory(
            UserModel,
            fields=['first_name', 'last_name', 'email'],
            labels={'first_name': 'Imię', 'last_name': 'Nazwisko'}
            )
        form = UserForm(request.POST, instance=request.user)
        user = form.save()
        return redirect('accounts:user_detail', owner.username)
