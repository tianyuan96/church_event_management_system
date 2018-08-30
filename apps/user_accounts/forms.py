from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

class RegisterUserForm(UserCreationForm):


    def username_taken(self):

        email = self.data['email']
        try:
            User._default_manager.get(username=email)
        except User.DoesNotExist:
            return False, ''

        return True, 'That email is already registered'

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', )

class LoginUserForm(forms.Form):

    email = forms.EmailField(max_length=254, help_text='Required. Please use a valid email address.')
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', )
