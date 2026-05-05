from django import forms
from django.core.exceptions import ValidationError


class SecretPhraseForm(forms.Form):
    secret_phrase = forms.CharField(
        max_length=255,
        label='Secret phrase',
        widget=forms.PasswordInput(attrs={'autocomplete': 'off'})
    )

    def clean_secret_phrase(self):
        secret_phrase = self.cleaned_data.get('secret_phrase')
        if secret_phrase and len(secret_phrase) < 12:
            raise ValidationError(f'Secret phrase must be at least 12 characters. Current length: {len(secret_phrase)}')
        return secret_phrase
