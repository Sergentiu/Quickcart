from django import forms
from django.contrib.auth.models import User

class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']