from django.shortcuts import render, get_object_or_404
from .models import Goal, Piece
from django.views.generic import ListView
from django.views import View

class GoalsView(ListView):
    template_name = "tracker/goals.html"
    model = Goal

class GoalDetailView(View):
    def get(self, request, pk):
        goal = get_object_or_404(Goal, pk=pk)
        return render(request, 'tracker/goal.html', {'goal': goal})

class PiecesView(View):
    def get(self, request):
        query_set = Piece.objects.all()
        return render(request, 'tracker/pieces.html', {'piece_list': query_set})