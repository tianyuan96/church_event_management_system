from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import os
# Create your models here.

def get_image_path(insance, filename):
    return os.path.join('image', str(insance.id), filename)

class Event(models.Model):

    name = models.CharField(max_length = 100)
    date = models.DateField(blank = True, default="1997-11-1")
    location = models.CharField(max_length = 100, default = "Some location")
    description = RichTextField(max_length=512,default = "")
    imageFile = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    host = models.ForeignKey(User, on_delete = models.CASCADE)

class InvolvedEvent(models.Model):

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)

    @classmethod
    def create(self):
        pass



class Post(models.Model):
    author = models.ForeignKey(User, on_delete= models.CASCADE)
    eventID = models.ForeignKey(Event, on_delete= models.CASCADE)
    date = models.DateTimeField(blank=True, default= "2006-10-25 14:30:59")
    imageFile = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    message = models.CharField(max_length = 256)
