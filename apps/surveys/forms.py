from django import forms
from .models import Survey

class CreateSurveyForm(forms.ModelForm):
    title = forms.CharField()

    class Meta:
        model = Survey
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }
