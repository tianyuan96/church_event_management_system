from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



states = [
    ('NSW', 'NSW'),
    ('VIC', 'VIC'),
    ('ACT', 'ACT'),
    ('TAS', 'TAS'),
    ('WA', 'WA'),
    ('NT', 'NT'),
]

class RegisterOrganisationForm(UserCreationForm):

    organisation = forms.CharField()

    def username_taken(self):

        email = self.data['email']
        try:
            User._default_manager.get(username=email)
        except User.DoesNotExist:
            return False, ''

        return True, 'That email is already registered'


    class Meta:
        model = User
        fields = ('organisation', 'email', 'password1', 'password2', )


class LoginOrganisationForm(forms.Form):

    email = forms.EmailField(max_length=254, help_text='Required. Please use a valid email address.')
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email', )

class OrgnasationForm(forms.ModelForm):

    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'required': 'required', }))
    display_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'required': False, }))

    # new_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class':'form-control',}))
    # confirm_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class':'form-control', }))

    class Meta:
        model = User
        # exclude = ('password',)
        fields = ('email', 'display_name',)