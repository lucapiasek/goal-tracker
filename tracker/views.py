from django.shortcuts import render, get_object_or_404, redirect
from .models import Goal, Piece
from .forms import GoalCreateForm, GoalUpdateForm
from django.views.generic import ListView
from django.views import View
from django.contrib.auth import get_user_model
import datetime

UserModel = get_user_model()

def is_owner(user, owner):
    return user.id == owner.id

def is_teacher(user, owner):
    if user.teacher.is_teacher:
        return user.teacher.students.all().contains(owner)

class GoalListView(ListView):
    template_name = "tracker/goal_list.html"
    model = Goal

    def get_queryset(self):
        owner = UserModel.objects.get(username=self.kwargs['username'])
        return Goal.objects.filter(user=owner)

class GoalDetailView(View):
    def get(self, request, username, pk):
        goal = get_object_or_404(Goal, pk=pk)
        return render(request, 'tracker/goal_detail.html', {'goal': goal, 'page_title': 'Cel'})

class GoalCreateView(View):
    def get(self, request, username):
        owner = UserModel.objects.get(username=username)
        date = request.session.get('last_visited_date', None)
        if date:
            date = datetime.date(**date)
        form = GoalCreateForm(user=owner, initial={
            'date': date
        })
        return render(request, 'tracker/create_form.html', {'form': form, 'page_title': 'Dodaj cel'})

    def post(self, request, username):
        owner = get_object_or_404(UserModel, username=username)
        form = GoalCreateForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            piece = cleaned_data['piece']
            pieces = cleaned_data['pieces']
            del cleaned_data['piece']
            del cleaned_data['pieces']
            cleaned_data['user'] = owner
            goal = Goal.objects.create(**cleaned_data)
            if piece:
                goal.pieces.create(name_to_display=f"{piece}", user=owner)
            if pieces.exists():
                goal.pieces.add(pieces)

            return redirect('tracker:goal_list')
        return render(request, 'tracker/create_form.html', {'form': form})

class GoalUpdateView(View):
    def get(self, request, username, pk):
        owner = get_object_or_404(UserModel, username=username)
        goal = get_object_or_404(Goal, pk=pk)
        form = GoalUpdateForm(instance=goal, user=owner)
        return render(request, 'tracker/create_form.html', {'form': form})

    def post (self, request, username, pk):
        goal = get_object_or_404(Goal, pk=pk)
        form = GoalUpdateForm()
        if form.is_valid():
            form.save()

class GoalDeleteView(View):
    def get(self, request, username, pk):
        goal = get_object_or_404(Goal, pk=pk)
        return render(request, 'delete_form.html', {'goal': goal})

    def post(self, request, username, pk):
        if request.POST('operation') == 'Tak':
            goal = get_object_or_404(Goal, pk=pk)
            goal.delete()
        return redirect('tracker:goal_list')

class PiecesView(View):
    def get(self, request):
        queryset = Piece.objects.all()
        return render(request, 'tracker/pieces.html', {'piece_list': queryset})