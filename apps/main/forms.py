from .models import MainPage
from django import forms
from ckeditor.widgets import CKEditorWidget


class MainPageForm(forms.ModelForm):

    class Meta:
        model = MainPage
        fields = ["description","imageFile",]
        fields = {
            'description': CKEditorWidget(attrs={'class': 'form-control'}),
            'imageFile': forms.FileInput(attrs={'class': 'custom-file-input'}),
            }