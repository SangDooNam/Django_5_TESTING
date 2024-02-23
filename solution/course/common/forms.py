"""Common forms to various apps."""

from django import forms


class LoginForm(forms.Form):
    """A simple login form."""

    user_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
