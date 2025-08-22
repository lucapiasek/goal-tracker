from django.shortcuts import render, get_object_or_404, redirect
from .models import Goal, Piece, PieceInformation
from .forms import GoalCreateForm, GoalUpdateForm, PieceCreateForm, PieceInformationCreateForm
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
    return False

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
        return render(request, 'tracker/create_form.html', {'form': form})

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
    def get(self, request, username):
        owner = get_object_or_404(UserModel, username=username)
        forms = [PieceCreateForm(user=owner), PieceInformationCreateForm()]
        return render(request, 'tracker/piece_create.html', {'forms': forms})

    def post(self, request, username):
        owner = get_object_or_404(UserModel, username=username)
        piece_form = PieceCreateForm(request.POST, user=owner)
        piece_information_form = PieceInformationCreateForm(request.POST)
        if piece_form.is_valid():
            piece = piece_form.save(commit=False)
            piece.user = owner
            piece.save()
            piece_form.save_m2m()
            if piece_information_form.is_valid():
                piece_information = piece_information_form.save(commit=False)
                piece_information.piece_id = piece.pk
                piece_information.save()
                piece_information_form.save_m2m()
                piece.pieceinformation = piece_information
                piece.save()
            return redirect('tracker:piece_list', username)
        forms = [piece_form, piece_information_form]
        return render(request, 'tracker/piece_create.html', {'forms': forms})


class PieceUpdateView(View):
    def get(self, request, username, pk):
        owner = get_object_or_404(UserModel, username=username)
        piece = get_object_or_404(Piece, pk=pk)
        piece_form = PieceCreateForm(instance=piece, user=owner)
        try:
            piece_information = PieceInformation.objects.get(piece=piece)
            piece_information_form = PieceInformationCreateForm(instance=piece_information, user=owner)
        except PieceInformation.DoesNotExist:
            piece_information_form = PieceInformationCreateForm(user=owner)

        forms = [piece_form, piece_information_form]
        return render(request, 'tracker/piece_create.html', {'forms': forms})

    def post(self, request, username, pk):
        owner = get_object_or_404(UserModel, username=username)
        piece = get_object_or_404(Piece, pk=pk)
        piece_form = PieceCreateForm(request.POST, instance=piece, user=owner)
        try:
            piece_information = PieceInformation.objects.get(piece=piece)
            piece_information_form = PieceInformationCreateForm(request.POST, instance=piece_information, user=owner)
        except PieceInformation.DoesNotExist:
            piece_information_form = PieceInformationCreateForm(request.POST, user=owner)

        if piece_form.is_valid():
            piece = piece_form.save(commit=False)
            piece.save()
            piece_form.save_m2m()
            if piece_information_form.is_valid():
                piece_information = piece_information_form.save(commit=False)
                piece_information.piece_id = piece.pk
                piece_information.save()
                piece_information_form.save_m2m()
                piece.pieceinformation = piece_information
                piece.save()
            return redirect('tracker:piece_detail', username, piece.pk)
        forms = [piece_form, piece_information_form]
        return render(request, 'tracker/piece_create.html', {'forms': forms})

class PieceDeleteView(View):
    def get(self, request, username, pk):
        piece = get_object_or_404(Piece, pk=pk)
        return render(request, 'tracker/delete_form.html', {'object_to_delete': piece})

    def post(self, request, username, pk):
        if request.POST.get('operation') == 'Tak':
            goal = get_object_or_404(Piece, pk=pk)
            goal.delete()
        return redirect('tracker:piece_list', username)