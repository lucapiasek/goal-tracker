from django.shortcuts import render, get_object_or_404, redirect
from .models import Goal, Piece, PieceInformation, Style
from .forms import GoalCreateForm, GoalUpdateForm, PieceCreateForm, PieceInformationCreateForm
from django.views.generic import ListView
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from accounts.permissions import is_owner_or_is_teacher
from django.forms import modelform_factory
import datetime

UserModel = get_user_model()

class GoalListView(UserPassesTestMixin, ListView):
    template_name = "tracker/goal_list.html"
    model = Goal

    def test_func(self):
        return is_owner_or_is_teacher(self.request.user, self.kwargs['username'])

    def get_queryset(self):
        owner = get_object_or_404(UserModel, username=self.kwargs['username'])
        return Goal.objects.filter(user=owner)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner'] = get_object_or_404(UserModel, username=self.kwargs['username'])
        return context

class GoalDetailView(UserPassesTestMixin, View):
    def test_func(self):
        return is_owner_or_is_teacher(self.request.user, self.kwargs['username'])

    def get(self, request, username, pk):
        owner = UserModel.objects.get(username=username)
        goal = get_object_or_404(Goal, pk=pk)
        return render(request, 'tracker/goal_detail.html', {'goal': goal, 'owner': owner})

class GoalCreateView(UserPassesTestMixin, View):
    def test_func(self):
        return is_owner_or_is_teacher(self.request.user, self.kwargs['username'])

    def get(self, request, username):
        owner = UserModel.objects.get(username=username)
        form = GoalCreateForm(user=owner)
        return render(request, 'tracker/create_form.html', {'form': form, 'page_title': 'Dodaj cel', 'owner': owner})

    def post(self, request, username):
        owner = get_object_or_404(UserModel, username=username)
        form = GoalCreateForm(request.POST, user=owner)
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

            return redirect('tracker:goal_list', owner.username)
        return render(request, 'tracker/create_form.html', {'form': form, 'page_title': 'Dodaj cel', 'owner': owner})

class GoalUpdateView(UserPassesTestMixin, View):
    def test_func(self):
        return is_owner_or_is_teacher(self.request.user, self.kwargs['username'])

    def get(self, request, username, pk):
        owner = get_object_or_404(UserModel, username=username)
        goal = get_object_or_404(Goal, pk=pk)
        form = GoalUpdateForm(instance=goal, user=owner)
        return render(request, 'tracker/create_form.html', {'form': form, 'page_title': 'Zaktualizuj cel', 'owner': owner})

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
        return render(request, 'tracker/create_form.html', {'form': form, 'page_title': 'Zaktualizuj cel', 'owner': owner})

class GoalDeleteView(UserPassesTestMixin, View):
    def test_func(self):
        return is_owner_or_is_teacher(self.request.user, self.kwargs['username'])

    def get(self, request, username, pk):
        owner = get_object_or_404(username=username)
        goal = get_object_or_404(Goal, pk=pk)
        return render(request, 'tracker/delete_form.html', {'object_to_delete': goal, 'owner':owner})

    def post(self, request, username, pk):
        if request.POST.get('operation') == 'Tak':
            goal = get_object_or_404(Goal, pk=pk)
            goal.delete()
        return redirect('tracker:goal_list', username)

class PieceListView(UserPassesTestMixin, View):
    def test_func(self):
        return is_owner_or_is_teacher(self.request.user, self.kwargs['username'])

    def get(self, request, username):
        owner = get_object_or_404(UserModel, username=username)
        queryset = Piece.objects.filter(user=owner)
        return render(request, 'tracker/piece_list.html', {'piece_list': queryset, 'username': username, 'owner': owner})

class PieceDetailView(UserPassesTestMixin, View):
    def test_func(self):
        return is_owner_or_is_teacher(self.request.user, self.kwargs['username'])

    def get(self, request, username, pk):
        owner = get_object_or_404(UserModel, username=username)
        piece = get_object_or_404(Piece, pk=pk)
        return render(request, 'tracker/piece_detail.html', {'piece': piece, 'owner': owner})

class PieceCreateView(UserPassesTestMixin, View):
    def test_func(self):
        return is_owner_or_is_teacher(self.request.user, self.kwargs['username'])

    def get(self, request, username):
        owner = get_object_or_404(UserModel, username=username)
        forms = [PieceCreateForm(user=owner), PieceInformationCreateForm()]
        return render(request, 'tracker/piece_create.html', {'forms': forms, 'owner': owner})

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
        return render(request, 'tracker/piece_create.html', {'forms': forms,  'owner': owner})

class PieceUpdateView(UserPassesTestMixin, View):
    def test_func(self):
        return is_owner_or_is_teacher(self.request.user, self.kwargs['username'])

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
        return render(request, 'tracker/piece_create.html', {'forms': forms, 'owner': owner})

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
        return render(request, 'tracker/piece_create.html', {'forms': forms, 'owner': owner})

class PieceDeleteView(UserPassesTestMixin, View):
    def test_func(self):
        return is_owner_or_is_teacher(self.request.user, self.kwargs['username'])

    def get(self, request, username, pk):
        owner = get_object_or_404(UserModel, username=username)
        piece = get_object_or_404(Piece, pk=pk)
        return render(request, 'tracker/delete_form.html', {'object_to_delete': piece, 'owner': owner})

    def post(self, request, username, pk):
        if request.POST.get('operation') == 'Tak':
            goal = get_object_or_404(Piece, pk=pk)
            goal.delete()
        return redirect('tracker:piece_list', username)

class StyleListView(UserPassesTestMixin, ListView):
    template_name = "tracker/basic_list.html"
    model = Style
    context_object_name = "object_list"

    def test_func(self):
        return is_owner_or_is_teacher(self.request.user, self.kwargs['username'])

    def get_queryset(self):
        owner = get_object_or_404(UserModel, username=self.kwargs['username'])
        return Style.objects.filter(user=owner)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner'] = get_object_or_404(UserModel, self.kwargs['username'])
        context['model_name'] = {
            'singular': 'styl',
            'plural': 'style'
        }
        context['links'] = {
            'create': 'tracker:style_create',
            'update': 'tracker:style_update'
        }
        return context

class StyleCreateView(UserPassesTestMixin, View):
    def test_func(self):
        return is_owner_or_is_teacher(self.request.user, self.kwargs['username'])

    def get(self, request, username):
        owner = get_object_or_404(UserModel, username=username)
        StyleForm = modelform_factory(Style, fields=["style"], labels={"style": "Styl"})
        return render(request, 'tracker/create_form.html', {'form': StyleForm, 'owner': owner})

    def post(self, request, username):
        owner = get_object_or_404(UserModel, username=username)
        StyleForm = modelform_factory(Style, fields=["style"], labels={"style": "Styl"})
        form = StyleForm(request.POST)
        style = form.save(commit=False)
        style.user = owner
        form.save()
        return redirect('tracker:style_list', username)

class StyleUpdateView(UserPassesTestMixin, View):
    def test_func(self):
        return is_owner_or_is_teacher(self.request.user, self.kwargs['username'])

    def get(self, request, username, pk):
        owner = get_object_or_404(UserModel, username=username)
        style = get_object_or_404(Style, pk=pk)
        StyleForm = modelform_factory(Style, fields=["style"], labels={"style": "Styl"})
        form = StyleForm(instance=style)
        return render(request, 'tracker/create_form.html', {'form': form, 'owner': owner})

    def post(self, request, username, pk):
        owner = get_object_or_404(UserModel, username=username)
        style = get_object_or_404(Style, pk=pk)
        StyleForm = modelform_factory(Style, fields=["style"], labels={"style": "Styl"})
        form = StyleForm(request.POST, instance=style)
        style = form.save(commit=False)
        style.user = owner
        form.save()
        return redirect('tracker:style_list', username)

class StyleDeleteView(UserPassesTestMixin, View):
    def test_func(self):
        return is_owner_or_is_teacher(self.request.user, self.kwargs['username'])

    def get(self, request, username, pk):
        owner = get_object_or_404(UserModel, username=username)
        style = get_object_or_404(Style, pk=pk)
        return render(request, 'tracker/delete_form.html', {'object_to_delete': style, 'owner': owner})