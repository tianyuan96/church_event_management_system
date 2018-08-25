from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    # username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text='Required. Please use a valid email address.')

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', )


class LoginUserForm(forms.Form):

    email = forms.EmailField(max_length=254, help_text='Required. Please use a valid email address.')
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', )
