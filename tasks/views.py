from django.shortcuts import render, get_object_or_404, redirect
from tracker.models import Task, Practice
from .forms import TaskForm, PracticeForm
from django.views.generic import ListView
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from accounts.permissions import is_owner_or_is_teacher, is_owner
from django.forms import modelform_factory
import datetime

UserModel = get_user_model()

class TaskListView(UserPassesTestMixin, View):
    def test_func(self):
        return is_owner_or_is_teacher(self.request.user, self.kwargs['username'])

    def get(self, request, username):
        owner = get_object_or_404(UserModel, username=self.kwargs['username'])
        task_list =  Task.objects.filter(user=owner)
        return render(request, "tasks/task_list.html", {
            'task_list': task_list,
            'owner': owner
        })

class TaskDetailView(UserPassesTestMixin, View):
    def test_func(self):
        return is_owner(self.request.user, self.kwargs['username'])

    def get(self, request, *args, **kwargs):
        owner = get_object_or_404(UserModel, username=kwargs['username'])
        task = get_object_or_404(Task, pk=kwargs['pk'])
        return render(request, 'tasks/task_detail.html', {'task': task, 'owner': owner})

class TaskCreateView(UserPassesTestMixin, View):
    def test_func(self):
        return is_owner_or_is_teacher(self.request.user, self.kwargs['username'])

    def get(self, request, *args, **kwargs):
        owner = get_object_or_404(UserModel, username=kwargs['username'])
        forms = [TaskForm(user=owner), PracticeForm()]
        return render(request, 'tasks/create_forms.html', {'forms': forms, 'owner': owner, 'page_title': 'Utwórz ćwiczenie'})

    def post(self, request, *args, **kwargs):
        owner = get_object_or_404(UserModel, username=kwargs['username'])
        task_form = TaskForm(request.POST, user=owner)
        practice_form = PracticeForm(request.POST)
        if task_form.is_valid():
            task = task_form.save(commit=False)
            task.user = owner
            task.save()
            if practice_form.is_valid():
                practice = practice_form.save(commit=False)
                practice.task_id = task.pk
                practice.save()
                task.practice_set.add(practice)
                task.was_practiced = True
                task.save()
            return redirect('tasks:list', kwargs['username'])
        forms = [task_form, practice_form]
        return render(request, 'tasks/create_forms.html', {'forms': forms, 'owner': owner, 'page_title': 'Utwórz ćwiczenie'})

class TaskUpdateView(UserPassesTestMixin, View):
    def test_func(self):
        return is_owner_or_is_teacher(self.request.user, self.kwargs['username'])

    def get(self, request, *args, **kwargs):
        owner = get_object_or_404(UserModel, username=kwargs['username'])
        task = get_object_or_404(Task, pk=kwargs['pk'])
        form = TaskForm(instance=task, user=owner)
        return render(request, 'tasks/create_form.html', {'form': form, 'page_title': 'Zaktualizuj zadanie', 'owner': owner})

    def post (self, request, *args, **kwargs):
        owner = get_object_or_404(UserModel, username=kwargs['username'])
        task = get_object_or_404(Task, pk=kwargs['pk'])
        form = TaskForm(request.POST, user=owner, instance=task)
        task = form.save()
        return redirect('tasks:detail', kwargs['username'], kwargs['pk'])

class TaskDeleteView(UserPassesTestMixin, View):
    def test_func(self):
        return is_owner_or_is_teacher(self.request.user, self.kwargs['username'])

    def get(self, request, *args, **kwargs):
        owner = get_object_or_404(UserModel, username=kwargs['username'])
        task = get_object_or_404(Task, pk=kwargs['pk'])
        return render(request, 'tasks/delete_form.html', {'object_to_delete': task, 'owner':owner})

    def post(self, request, *args, **kwargs):
        if request.POST.get('operation') == 'Tak':
            task = get_object_or_404(Task, pk=kwargs['pk'])
            task.delete()
        return redirect('tasks:list', kwargs['username'])

class PracticeCreateView(UserPassesTestMixin, View):
    def test_func(self):
        return is_owner(self.request.user, self.kwargs['username'])

    def get(self, request, *args, **kwargs):
        owner = get_object_or_404(UserModel, username=kwargs['username'])
        task = get_object_or_404(Task, pk=kwargs['pk'])
        form = PracticeForm()
        return render(request, 'tasks/practice_form.html',{
            'form': form,
            'page_title': 'Zaktualizuj zadanie',
            'owner': owner,
            'task': task})

    def post(self, request, *args, **kwargs):
        owner = get_object_or_404(UserModel, username=kwargs['username'])
        task = get_object_or_404(Task, pk=kwargs['pk'])
        form = PracticeForm(request.POST)
        practice = form.save(commit=False)
        practice.task = task
        form.save()
        task.was_practiced = True
        task.save()
        return redirect('tasks:detail', kwargs['username'], task.pk)

class PracticeUpdateView(UserPassesTestMixin, View):
    def test_func(self):
        return is_owner(self.request.user, self.kwargs['username'])

    def get(self, request, *args, **kwargs):
        owner = get_object_or_404(UserModel, username=kwargs['username'])
        practice = get_object_or_404(Practice, pk=kwargs['pk'])
        task = get_object_or_404(Task, pk=practice.task.pk)
        form = PracticeForm(instance=practice)
        return render(request, 'tasks/create_form.html',{
            'form': form,
            'page_title': 'Zaktualizuj zadanie',
            'owner': owner,
            'task': task})

    def post(self, request, *args, **kwargs):
        owner = get_object_or_404(UserModel, username=kwargs['username'])
        practice = get_object_or_404(Practice, pk=kwargs['pk'])
        task = get_object_or_404(Task, pk=practice.task.pk)
        form = PracticeForm(request.POST, instance=practice)
        practice = form.save(commit=False)
        practice.task.pk = task.pk
        form.save()
        return redirect('tasks:detail', kwargs['username'], task.pk)

class PracticeDeleteView(UserPassesTestMixin, View):
    def test_func(self):
        return is_owner_or_is_teacher(self.request.user, self.kwargs['username'])

    def get(self, request, *args, **kwargs):
        owner = get_object_or_404(UserModel, username=kwargs['username'])
        practice = get_object_or_404(Practice, pk=kwargs['pk'])
        return render(request, 'tasks/delete_form.html', {'object_to_delete': practice, 'owner':owner})

    def post(self, request, *args, **kwargs):
        if request.POST.get('operation') == 'Tak':
            practice = get_object_or_404(Practice, pk=kwargs['pk'])
            task_pk = practice.task.pk
            practice.delete()
        return redirect('tasks:detail', kwargs['username'], task_pk)

