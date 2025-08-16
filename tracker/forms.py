from django import forms
from django.core.exceptions import ValidationError
from .models import Piece, Goal

date_input_formats = [
        "%d.%m.%Y",
        "%d.%m.%y",
        "%d/%m/%Y",
        "%d/%m/%y",
        "%d-%m-%Y",
        "%d-%m-%y",
        "%d %m %Y",
        "%d %m %y",
        "%Y/%m/%d",
        "%Y.%m.%d"
    ]

class GoalCreateForm(forms.Form):
    name = forms.CharField(max_length=200, label='Cel', required=False, empty_value='')
    piece = forms.CharField(max_length=200, label='Utwór', required=False, empty_value='')
    pieces = forms.ModelMultipleChoiceField(queryset=Piece.objects.none(), label="Utwory", required=False, widget=forms.CheckboxSelectMultiple)
    date = forms.DateField(required=False, label='Data', input_formats=date_input_formats)
    time = forms.TimeField(label="Godz.", required=False)
    additional_info = forms.CharField(label="Dodatkowe informacje", required=False, )

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        piece = cleaned_data.get("piece")
        pieces = cleaned_data.get("pieces")
        additional_info = cleaned_data.get("additional_info")

        if not name and not piece and not pieces.exists() and not additional_info:
            err = ValidationError("Conajmniej jedno z tych pól musi być wypełnione")
            self.add_error("name", err)
            self.add_error("piece", err)
            self.add_error("pieces", err)
            self.add_error("additional_info", err)

class GoalUpdateForm(forms.ModelForm):
    pieces = forms.ModelMultipleChoiceField(queryset=Piece.objects.none(), label="Utwory", required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Goal
        use_required_attribute = False
        fields = ('name', 'date', 'time', 'is_concluded', 'additional_info')

    def init(self, *args, user=None, **kwargs):
        # Czy popować usera z kwargs?
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['pieces'].queryset = Pieces.objects.filter(user=user)

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        pieces = cleaned_data.get("pieces")
        additional_info = cleaned_data.get("additional_info")

        if not name and not pieces.exists() and not additional_info:
            err = ValidationError("Conajmniej jedno z tych pól musi być wypełnione")
            self.add_error("name", err)
            self.add_error("pieces", err)
            self.add_error("additional_info", err)