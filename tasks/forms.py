from django import forms
from django.core.exceptions import ValidationError
from tracker.models import Task, Practice, Goal, Piece


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        use_required_attribute = False
        fields = ('goal', 'piece', 'element', 'method', 'is_suggested')


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

class PracticeForm(forms.ModelForm):
    date = forms.DateField(required=True)

    class Meta:
        model = Practice
        use_required_attribute = False
        fields = ('date', 'start_time', 'end_time', 'repetitions', 'is_summarized', 'is_completed')
