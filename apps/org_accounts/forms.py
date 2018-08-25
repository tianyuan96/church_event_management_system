from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


states = [
    ('NSW', 'NSW'),
    ('VIC', 'VIC'),
    ('ACT', 'ACT'),
    ('TAS', 'TAS'),
    ('WA', 'WA'),
    ('NT', 'NT'),
]

class RegisterOrganisationForm(UserCreationForm):
    organisation = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Please use a valid email address.')
    # state = forms.OptionsField(choices=states)

    class Meta:
        model = get_user_model()
        fields = ('organisation', 'email', 'password1', 'password2', )
