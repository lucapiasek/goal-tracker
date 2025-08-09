from django.forms import Form

class GoalCreateForm(Form):
    @property
    def title(self):
        return "Cel"
