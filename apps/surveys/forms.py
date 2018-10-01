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
            'title': forms.TextInput(attrs={'class': 'form-control','id':'survey_tile'}),
        }


class CreateOptionForm(forms.ModelForm):


    class Meta:
        model = OptionInSurvey
        fields = ['name','description','imageFile']
        # exclude =('host',)

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','id': 'option_name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'id': 'option_description'}),
            'imageFile':forms.FileInput(attrs={'class': 'custom-file-input', 'id': 'option_imageFile'}),
        }