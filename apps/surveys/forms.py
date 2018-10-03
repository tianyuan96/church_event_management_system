from django import forms
from .models import Survey, FoodPreferences,OptionInSurvey
from ckeditor.widgets import CKEditorWidget

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
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'id':'survey_tile',
                                            'place holder' : 'Title of the event'})
        }

    def clean_title(self):
        title = self.cleaned_data["title"]
        if title == "":
            raise forms.ValidationError("the title can not be empty")
        else:
            return title


class CreateOptionForm(forms.ModelForm):


    class Meta:
        model = OptionInSurvey
        fields = ['name','description','imageFile']
        # exclude =('host',)
        description = forms.CharField()

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','id': 'option_name'}),
            'description': CKEditorWidget(attrs={'class': 'form-control', 'id': 'option_description'}),
            'imageFile':forms.FileInput(attrs={'class': 'custom-file-input', 'id': 'option_imageFile'}),
        }