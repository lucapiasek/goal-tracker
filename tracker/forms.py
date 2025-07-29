from django.forms import ModelForm
from tracker.models import Goal

class GoalCreateForm(ModelForm):
    class Meta:
        model = Goal
        fields = "__all__"