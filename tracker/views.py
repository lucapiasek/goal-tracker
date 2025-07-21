from django.shortcuts import render
from .models import Goal, Piece
from django.views.generic import ListView
from django.views import View

class GoalsView(ListView):
    template_name = "tracker/goals.html"
    model = Goal

class PiecesView(View):
    def get(self, request):
        query_set = Piece.objects.all()
        return render(request, 'tracker/pieces.html', {'piece_list': query_set})