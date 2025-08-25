from django import forms
from django.core.exceptions import ValidationError
from tracker.models import Challenge, Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        use_required_attribute = False
        fields = ('goal', 'piece', 'element', 'method')


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['goal'].queryset = Goal.objects.filter(user=user)
            self.fields['piece'].queryset = Piece.objects.filter(user=user)

    def clean(self):
        cleaned_data = super().clean()
        goal = cleaned_data.get("goal")
        piece = cleaned_data.get("piece")

        if not goal and not piece:
            err = ValidationError("Conajmniej jedno z tych pól musi być wypełnione")
            self.add_error("goal", err)
            self.add_error("pieces", err)

class ChallengeForm(forms.ModelForm):

    class Meta:
        model = Challenge
        use_required_attribute = False
        fields = ('start_date', 'minimum_number_of_days', 'minimum_number_of_repetitions', 'minimum_total_repetitions', 'is_completed')
