from django import forms

from users.models import User


class BaseAdminUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'is_active',
            'is_staff',
            'is_superuser',
        ]
        labels = {
            'is_superuser': 'Is Admin'
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

            if field_name in ('is_active', 'is_staff', 'is_superuser',):
                field.widget.attrs['class'] = 'form-check-input'

            if field.required:
                field.label += ' *'
