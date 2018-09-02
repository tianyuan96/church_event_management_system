from django.db import models

# Create your models here.


class Event(models.Model):

    name = models.CharField(max_length=100)
    date = models.DateField()
    location = models.CharField(max_length=100)
    description = models.CharField(max_length=512)


class InvolvedEvent(models.Model):

    eventId = models.ForeignKey(Event, on_delete=models.CASCADE)
    participant = models.ForeignKey(Event, on_delete=models.CASCADE)