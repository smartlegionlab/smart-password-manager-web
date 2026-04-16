from django import forms

from users.forms.user_base_form import BaseUserForm


class UserEditForm(BaseUserForm):
    class Meta(BaseUserForm.Meta):
        fields = BaseUserForm.Meta.fields
        labels = {
            **BaseUserForm.Meta.labels,
        }
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
