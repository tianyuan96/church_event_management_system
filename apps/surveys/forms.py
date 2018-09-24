from django import forms
from .models import Survey, FoodPreferences,OptionInSurvey

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


class CreateOptionForm(forms.ModelForm):


    class Meta:
        model = OptionInSurvey
        fields = ['name','description','imageFile']
        # exclude =('host',)

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'imageFile':forms.FileInput(attrs={'class': 'custom-file-input'}),
        }