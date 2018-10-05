from .models import Event, Post
from django import forms
import datetime
from ckeditor.widgets import CKEditorWidget

class EventCreationForm(forms.ModelForm):

    # Fields
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control',
                                           'type': 'date'}),
                           initial=datetime.date.today)

    class Meta:
        model = Event
        fields = ['name', 'location', 'description', 'imageFile', 'host','date',]
        # exclude = ('host',)

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.TextInput(attrs={'class': 'form-control',
                                           'type': 'date'}),
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
<<<<<<< HEAD
            'name': forms.TextInput(attrs={'class':'form-control'}),
=======
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.TextInput(attrs={'class': 'form-control',
                                           'type': 'date'}),
>>>>>>> newForums
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': CKEditorWidget(attrs={'class': 'form-control'}),
            'imageFile': forms.FileInput(attrs={'class': 'custom-file-input'}),

        }

class PostUpdateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = '__all__'
        fields = {

            'message': forms.Textarea(attrs={'class': 'form-control'}),
            'imageFile': forms.FileInput(attrs={'class': 'custom-file-input'}),
            }

class PostCreationForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = '__all__'
        fields = {
            'message': forms.Textarea(attrs={'class': 'form-control'}),
            'imageFile': forms.FileInput(attrs={'class': 'custom-file-input'}),
        }
