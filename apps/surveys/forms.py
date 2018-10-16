from django import forms
from .models import Survey, OptionInSurvey
from ckeditor.widgets import CKEditorWidget


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

    def __init__(self, *args, **kwargs):
        super(CreateOptionForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = False

    # def clean_name(self):
    #     name = self.cleaned_data["name"]
    #     if name == "":
    #         raise forms.ValidationError("the name of option can not be empty")
    #     else:
    #         return name



    class Meta:
        model = OptionInSurvey
        fields = ['name','description','imageFile']



        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','id': 'option_name'}),
            'description': CKEditorWidget(attrs={'class': 'form-control', 'id': 'option_description'}),
            'imageFile':forms.FileInput(attrs={'class': 'custom-file-input', 'id': 'option_imageFile'}),
        }
