from django import forms
from .models import Survey, FoodPreferences

class FoodPreferencesForm(forms.ModelForm):

    class Meta:

        model = FoodPreferences
        exclude = ('user', )

class CreateSurveyForm(forms.ModelForm):
    title = forms.CharField()

    class Meta:
        model = Survey
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }
