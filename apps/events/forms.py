from .models import Event
from django import forms
import datetime
class EventCreationForm(forms.ModelForm):

    # Fields
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control',
                                           'type': 'date'}),
                           initial=datetime.date.today)

    class Meta:
        model = Event
        fields = '__all__'
        # exclude = ('host',)

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'imageFile':forms.FileInput(attrs={'class': 'custom-file-input'})

        }


class EventUpdateForm(forms.ModelForm):

    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control',
                                                         'type': 'date'}))
    class Meta:

        model = Event
        fields = '__all__'
        fields = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'imageFile': forms.FileInput(attrs={'class': 'custom-file-input'}),

        }
