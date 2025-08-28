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
        invited_username = cleaned_data.get('invited')
        inviting_username = cleaned_data.get('inviting')
        invitation_type = cleaned_data.get('invitation_type')

        permitted_invitation_types = {'student': 'student', 'teacher': 'teacher'}

        if invitation_type not in permitted_invitation_types:
            raise ValidationError('Form tampered. Please do not do this.')

        try:
            invited_user = UserModel.objects.get(username=invited_username)
            inviting_user = UserModel.objects.get(username=inviting_username)
            if hasattr(inviting_user, invitation_type):
                removed_from_dict = permitted_invitation_types.pop(invitation_type)
                if hasattr(invited_user, [value for value in permitted_invitation_types.values()][0]):
                    error = ValidationError('Użytkownik już został zaproszony')
                    if invitation_type == 'student':
                        if invited_user.teacher.student_invitations.all().contains(inviting_user.student):
                            raise error
                    elif invitation_type == 'teacher':
                        if invited_user.student.teacher_invitations.all().contains(inviting_user.teacher):
                            raise error
        except UserModel.DoesNotExist:
            error = ValidationError("Podany użytkownik nie istnieje")
            self.add_error("invited", error)