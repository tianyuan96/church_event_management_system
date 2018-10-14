from django.db import models
from ckeditor.fields import RichTextField
import os


def get_image_path(insance, filename):
    return os.path.join('image', str(insance.id), filename)


class MainPage(models.Model):
    name = models.CharField(default="main_page",unique=True,max_length=20)
    description = RichTextField(max_length=512, blank=True)
    imageFile = models.ImageField(upload_to=get_image_path, blank=True, null=True)