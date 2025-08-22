from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm
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
            return redirect('tracker_calendar:year_view', request.user.username, timezone.now().year)
        return render(request, 'accounts/create_form.html', {'form': form, 'page_title': "Zarejestruj się"})

class LogoutView(View):
    def get(self):
        def get(self):
            return render(request, 'accounts/logout_form.html')