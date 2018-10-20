from .models import Event, Post, ReplyTo
from django import forms
import datetime
from ckeditor.widgets import CKEditorWidget

class EventCreationForm(forms.ModelForm):

    # Fields
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control',
                                           'type': 'date'}),
                           initial=datetime.date.today)
    def clean_date(self):
        date = self.cleaned_data['date']
        if date < datetime.date.today():
            raise forms.ValidationError("The date cannot be in the past")
        else:
            return date

    class Meta:
        model = Event
        fields = ['name', 'location', 'description', 'imageFile', 'host','date','lan','lng']

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control','id':'location_input'}),
            'description': CKEditorWidget(attrs={'class': 'form-control'}),
            'imageFile':forms.FileInput(attrs={'class': 'custom-file-input'}),
            'lan':forms.TextInput(attrs={'class':'form-control','type':'hidden',"id":"lan"}),
            'lng':forms.TextInput(attrs={'class':'form-control','type':'hidden',"id":"lng"}),
        }


class EventUpdateForm(forms.ModelForm):

    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control',
                                                         'type': 'date'}))
    lan = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control',  'type':'hidden','id': "lan"}))
    lng = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'hidden','id': "lng"}))

    class Meta:

        model = Event
        fields =['date','name','location','description','imageFile','lan','lng']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            # 'date': forms.TextInput(attrs={'class': 'form-control',
            #                                'type': 'date'}),
            'location': forms.TextInput(attrs={'class': 'form-control','id':'location_input'}),
            'description': CKEditorWidget(attrs={'class': 'form-control'}),
            'imageFile': forms.FileInput(attrs={'class': 'custom-file-input'}),

        }

class PostUpdateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['message', 'imageFile']
        widgets = {

            'message': CKEditorWidget(attrs={'class': 'form-control'}),
            'imageFile': forms.FileInput(attrs={'class': 'custom-file-input'}),
            }

class PostCreationForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['message', 'imageFile']
        widgets = {
            'message': CKEditorWidget(attrs={'class': 'form-control'}),
            'imageFile': forms.FileInput(attrs={'class': 'custom-file-input', 'id': 'post_image'}),
        }

class ReplyCreationForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'message': CKEditorWidget(attrs={'class': 'form-control'}),
        }
