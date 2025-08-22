from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.utils import timezone

class UserCreateView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'accounts/create_form.html', {'form': form, 'page_title': "Zarejestruj się"})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tracker_calendar:year', request.user.username, timezone.now().year)
        return render(request, 'accounts/create_form.html', {'form': form, 'page_title': "Zarejestruj się"})

class LoginView(LoginView):
    template_name = 'accounts/create_form.html',
    next_page = 'tracker:goals',
    extra_context = {'page_title': "Zaloguj się"}

class LogoutView(View):
    def get(self, request):
        def get(self):
            return render(request, 'accounts/logout_form.html')
    def post(self, request):
        logout(request)
        return redirect('accounts:login')