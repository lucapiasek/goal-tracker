from django.forms import ModelForm
from tracker.models import Goal

class GoalCreateForm(ModelForm):
    @property
    def title(self):
        return "Cel"

    class Meta:
        model = Goal
        fields = "__all__"

