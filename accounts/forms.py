from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


UserModel = get_user_model()

class InvitationForm(forms.Form):
    invited = forms.CharField(required=True, label="Wpisz username osoby, którą chcesz zaprosić", max_length=50)
    inviting = forms.CharField(max_length=50, widget=forms.HiddenInput, disabled=True)
    invitation_type = forms.CharField(max_length=20, widget=forms.HiddenInput, disabled=True)


    def clean(self):
        cleaned_data = super().clean()
        invited = cleaned_data.get('invited')
        inviting = cleaned_data.get('inviting')
        invitation_type = cleaned_data.get('invitation_type')

        permitted_invitation_types = ['student', 'teacher']

        if invitation_type not in permitted_invitation_types:
            raise ValidationError('Form tampered. Please do not do this.')

        try:
            invited_user = UserModel.objects.get(username=invited)
            inviting_user = UserModel.objects.get(username=inviting)
            if hasattr(invited_user, invitation_type):
                permitted_invitation_types.pop(invitation_type)
                if hasattr(inviting_user, invitation_type):
                    error = ValidationError('Użytkownik już został zaproszony')
                    if invitation_type == 'student':
                        if invited_user.teacher.student_invitations.all().contains(inviting.student):
                            raise error
                    elif invitation_type == 'teacher':
                        if invited_user.student.teacher_invitations.all().contains(inviting.teacher):
                            raise error
        except UserModel.DoesNotExist:
            error = ValidationError("Podany użytkownik nie istnieje")
            self.add_error("invited", error)