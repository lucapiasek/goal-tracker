from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm

class UserCreateView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'accounts/create_form.html', {'form': form, 'page_title': "Zarejestruj się"})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tracker:goal_list', request.user.username)
        return render(request, 'accounts/create_form.html', {'form': form, 'page_title': "Zarejestruj się"})