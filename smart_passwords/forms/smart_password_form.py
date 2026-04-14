from django import forms
from django.core.exceptions import ValidationError

from smart_passwords.models import SmartPassword


class SmartPasswordForm(forms.ModelForm):
    secret_phrase = forms.CharField(
        max_length=255,
        label='Secret phrase',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter your secret phrase (min. 12 characters)'}),
        help_text='Minimum 12 characters. Example: "MyCat🐱Hippo2026" or "P@ssw0rd!LongSecret"'
    )
    length = forms.IntegerField(
        min_value=12,
        max_value=100,
        label='Password Length',
        initial=16,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 12, 'max': 100})
    )

    class Meta:
        model = SmartPassword
        fields = ['description', 'secret_phrase', 'length', ]

    def clean_secret_phrase(self):
        secret_phrase = self.cleaned_data.get('secret_phrase')
        if secret_phrase and len(secret_phrase) < 12:
            raise ValidationError(f'Secret phrase must be at least 12 characters. Current length: {len(secret_phrase)}')
        return secret_phrase
