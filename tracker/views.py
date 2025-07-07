from django.shortcuts import render
from .models import Goal
from django.views.generic import ListView

class GoalsView(ListView):
    template_name = "tracker/goals.html"
    model = Goal