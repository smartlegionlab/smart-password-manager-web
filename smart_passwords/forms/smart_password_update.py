from django import forms

from smart_passwords.models import SmartPassword


class SmartPasswordUpdateForm(forms.ModelForm):
    length = forms.IntegerField(
        min_value=12,
        max_value=100,
        label='Password Length',
        initial=16,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 12, 'max': 100})
    )

    class Meta:
        model = SmartPassword
        fields = ['description', 'length', ]
