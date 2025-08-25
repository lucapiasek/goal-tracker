from django.shortcuts import render, get_object_or_404, redirect
from tracker.models import Task
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from accounts.permissions import is_owner


UserModel = get_user_model()

class SuggestionsListView(UserPassesTestMixin, View):
    def test_func(self):
        return is_owner(self.request.user, self.kwargs['username'])

    def get(self, request, username):
        owner = get_object_or_404(UserModel, username=self.kwargs['username'])
        suggested_task_list =  Task.objects.filter(user=owner).filter(are_suggestions_enabled=True).filter(is_suggested=True)
        return render(request, "suggestions/task_list.html", {
            'task_list': suggested_task_list,
            'owner': owner
        })