from django.shortcuts import render, get_object_or_404, redirect
from tracker.models import Challenge, Task
from .forms import ChallengeForm
from tasks.forms import TaskForm
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from accounts.permissions import is_owner_or_is_teacher, is_teacher, is_student

UserModel = get_user_model()

class ChallengeListView(UserPassesTestMixin, View):
    def test_func(self):
        return is_owner_or_is_teacher(self.request.user, self.kwargs['username'])

    def get(self, request, username):
        owner = get_object_or_404(UserModel, username=username)
        challenge_list =  Challenge.objects.filter(user=owner)
        return render(request, "challenges/challenge_list.html", {
            'challenge_list': challenge_list,
            'owner': owner
        })

class ChallengeDetailView(UserPassesTestMixin, View):
    def test_func(self):
        return is_owner_or_is_teacher(self.request.user, self.kwargs['username'])

    def get(self, request, username, pk):
        owner = get_object_or_404(UserModel, username=username)
        challenge = get_object_or_404(Challenge, pk=pk)
        task = Task.objects.select_related('challenge')
        return render(request, 'challenges/challenge_detail.html', {'challenge': challenge, 'task': task, 'owner': owner})

class ChallengeCreateView(UserPassesTestMixin, View):
    def test_func(self):
        return is_owner_or_is_teacher(self.request.user, self.kwargs['username'])

    def get(self, request, username):
        owner = get_object_or_404(UserModel, username=username)
        forms = [TaskForm(user=owner), ChallengeForm()]
        return render(request, 'challenges/create_forms.html', {'forms': forms, 'owner': owner})

    def post(self, request, username):
        owner = get_object_or_404(UserModel, username=username)
        task_form = TaskForm(request.POST, user=owner)
        challenge_form = ChallengeForm(request.POST)
        task = task_form.save(commit=False)
        task.user = owner
        task.save()
        challenge = challenge_form.save(commit=False)
        challenge.task.pk = task.pk
        challenge.user = owner
        challenge.save()
        task.challenge = challenge
        task.save()
        return redirect('challenges:list', username)

class ChallengeCreateFromTaskView(UserPassesTestMixin, View):
    def test_func(self):
        return is_owner_or_is_teacher(self.request.user, self.kwargs['username'])

    def get(self, request, username, task_id):
        owner = get_object_or_404(UserModel, username=username)
        task = get_object_or_404(Task, pk=task_id)
        forms = [TaskForm(user=owner, instance=task), ChallengeForm()]
        return render(request, 'challenges/create_forms.html', {'forms': forms, 'owner': owner, 'page_title': 'Utwórz wyzwanie'})

    def post(self, request, username, task_id):
        owner = get_object_or_404(UserModel, username=username)
        task_form = TaskForm(request.POST, user=owner)
        challenge_form = ChallengeForm(request.POST)
        task = task_form.save(commit=False)
        task.user = owner
        task.save()
        challenge = challenge_form.save(commit=False)
        challenge.task = task
        challenge.user = owner
        challenge.save()
        task.challenge = challenge
        task.save()
        return redirect('challenges:list', username)

class ChallengeDeleteView(UserPassesTestMixin, View):
    def test_func(self):
        return is_owner_or_is_teacher(self.request.user, self.kwargs['username']) and not is_student(self.request.user, self.kwargs['username'])

    def get(self, request, username, pk):
        owner = get_object_or_404(username=username)
        challenge = get_object_or_404(Challenge, pk=pk)
        return render(request, 'tasks/delete_form.html', {'object_to_delete': challenge, 'owner':owner})

    def post(self, request, username, pk):
        if request.POST.get('operation') == 'Tak':
            challenge = get_object_or_404(Challenge, pk=pk)
            challenge.delete()
        return redirect('challenge:list', username)

class ChallengeConfirmView(UserPassesTestMixin, View):
    def test_func(self):
        return is_teacher(self.request.user.username, self.kwargs['username'])

    def get(self, request, username, pk):
        owner = get_object_or_404(UserModel, username=username)
        challenge = get_object_or_404(Challenge, pk=pk)

        if challenge.check_if_fulfilled():
            challenge.set_are_requirements_fulfilled()
            question = f"Czy chcesz potwierdzić wykonanie wyzwania {challenge}?"
        else:
            question = f"Wymagania nie został spełnione. Czy pomimo to chcesz potwierdzić wykonanie wyzwania {challenge}?"
        return render(request, 'challenges/confirmation_form.html', {
            'question': question,
            'owner': owner
        })

    def post(self, request, username, pk):
        owner = get_object_or_404(UserModel, username=username)
        challenge = get_object_or_404(Challenge, pk=pk)
        if request.POST['operation'] == 'Tak':
            challenge.is_completed = True
            return render(request, "challenges/success.html", {
                'owner': owner,
                'success_message': 'Wyzwanie zostało zaliczone'
            })
        return redirect('challenges:detail', owner.username, challenge.pk)
