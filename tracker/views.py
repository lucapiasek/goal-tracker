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
        owner = get_object_or_404(UserModel, username=self.kwargs['username'])
        return Goal.objects.filter(user=owner)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner_username'] = self.kwargs['username']
        return context

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
        owner = get_object_or_404(UserModel, username=username)
        goal = get_object_or_404(Goal, pk=pk)
        form = GoalUpdateForm(request.POST, user=owner, instance=goal)
        if form.is_valid():
            goal = form.save()
            pieces = form.cleaned_data['pieces']
            goal.pieces.set(pieces)
            goal.save()
        return redirect('tracker:goal_detail', username, pk)

class GoalDeleteView(View):
    def get(self, request, username, pk):
        goal = get_object_or_404(Goal, pk=pk)
        return render(request, 'tracker/delete_form.html', {'object_to_delete': goal})

    def post(self, request, username, pk):
        if request.POST.get('operation') == 'Tak':
            goal = get_object_or_404(Goal, pk=pk)
            goal.delete()
        return redirect('tracker:goal_list', username)

class PieceListView(View):
    def get(self, request, username):
        owner = get_object_or_404(UserModel, username=username)
        queryset = Piece.objects.filter(user=owner)
        return render(request, 'tracker/piece_list.html', {'piece_list': queryset, 'username': username})

class PieceDetailView(View):
    def get(self, request, username, pk):
        piece = get_object_or_404(Piece, pk=pk)
        return render(request, 'tracker/piece_detail.html', {'piece': piece})

class PieceCreateView(View):
    def get(self, request, username, pk):
        pass

class PieceUpdateView(View):
    pass

class PieceDeleteView(View):
    pass