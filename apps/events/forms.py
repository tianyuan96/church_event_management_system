from .models import Event
from django import forms

class EventCreationForm(forms.ModelForm):

    # Fields
    # model = Event
    # name = forms.CharField()


    class Meta:

        model = Event
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'date': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),

        }

