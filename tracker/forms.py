from django.forms import ModelForm
from tracker.models import Goal

class GoalCreateForm(ModelForm):
    @property
    def title(self):
        return f"{self._meta.model._meta.verbose_name.title()}"

    class Meta:
        model = Goal
        fields = "__all__"