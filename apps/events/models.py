from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Event(models.Model):

    name = models.CharField(max_length = 100)
    date = models.DateField(blank = True, default="1997-11-1")
    location = models.CharField(max_length = 100, default = "Some location")
    description = models.CharField(max_length=512,default = "Some location")
    host = models.OneToOneField(User, on_delete = models.CASCADE)


class InvolvedEvent(models.Model):

    eventId = models.ForeignKey(Event, on_delete = models.CASCADE)
    participant = models.ForeignKey(User, on_delete = models.CASCADE)