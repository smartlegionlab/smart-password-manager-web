from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError


class Enable2FAForm(forms.Form):
    verification_code = forms.CharField(
        max_length=6,
        min_length=6,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter 6-digit code',
            'autocomplete': 'off'
        }),
        label='Verification Code'
    )
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    
    def clean_verification_code(self):
        code = self.cleaned_data.get('verification_code')
        totp = self.user.get_totp_device()
        
        if not totp or not totp.verify(code, valid_window=1):
            raise ValidationError('Invalid verification code. Please try again.')
        
        return code


class Disable2FAForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        }),
        label='Password'
    )
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        user = authenticate(
            request=None,
            email=self.user.email,
            password=password
        )
        
        if not user:
            raise ValidationError('Invalid password. Please try again.')
        
        return password


class TwoFactorLoginForm(forms.Form):
    code = forms.CharField(
        max_length=8,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter 6-digit code or backup code',
            'autocomplete': 'off'
        }),
        label='Authentication Code'
    )
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    
    def clean_code(self):
        code = self.cleaned_data.get('code')
        
        if self.user.verify_totp(code):
            return code
        
        if self.user.verify_backup_code(code):
            return code
        
        raise ValidationError('Invalid authentication code. Please try again.')
