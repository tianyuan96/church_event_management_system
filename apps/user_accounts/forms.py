from django import forms
from django.contrib.auth import forms as auth_forms
# from django.contrib.auth.models import User
from apps.user_accounts import models
from django.contrib.auth.models import User



class RegisterUserForm(auth_forms.UserCreationForm):


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
        model = User
        fields = ('username', 'password', )

# class UserDetailsForm(forms.ModelForm):
#     # email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'required': 'required', }))
#
#     class Meta:
#         model = models.UserDetails
#         fields = ('display_name', )

class UserForm(forms.ModelForm):

    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'required': 'required', }))
    display_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'required': False, }))

    # new_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class':'form-control',}))
    # confirm_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class':'form-control', }))

    class Meta:
        model = User
        # exclude = ('password',)
        fields = ('email', 'display_name',)
