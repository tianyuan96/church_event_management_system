from .models import Event, Post
from django import forms

class EventCreationForm(forms.ModelForm):

    # Fields
    # model = Event
    # name = forms.CharField()
    class Meta:

        model = Event
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.TextInput(attrs={'class': 'form-control',
                                           'type': 'date'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'imageFile':forms.FileInput(attrs={'class': 'custom-file-input'})

        }

class EventUpdateForm(forms.ModelForm):

    # Fields
    # model = Event
    # name = forms.CharField()


    class Meta:

        model = Event
        fields = '__all__'
        fields = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.TextInput(attrs={'class': 'form-control',
                                           'type': 'date'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
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
