from django import forms
from django.contrib.auth.forms import UserCreationForm

from user.models import CustomUser

class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password1', 'password2']

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'your-email-class'}),
            'username': forms.TextInput(attrs={'class': 'your-username-class'}),
            'password1': forms.PasswordInput(attrs={'class': 'your-password-class'}),
            'password2': forms.PasswordInput(attrs={'class': 'your-password-confirm-class'}),
        }

