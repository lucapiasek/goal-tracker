from django import forms
from tracker.models import Challenge, Task


class ChallengeForm(forms.ModelForm):

    class Meta:
        model = Challenge
        use_required_attribute = False
        fields = ('start_date', 'minimum_number_of_days', 'minimum_number_of_repetitions', 'minimum_total_repetitions', 'is_completed')
