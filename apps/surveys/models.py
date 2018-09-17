from django.db import models
from django.contrib.auth.models import User
from apps.events.models import Event,InvolvedEvent

# Create your models here.

class FoodPreferences(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One user has one set of food prefs

    vegetarian = models.BooleanField(default=False)
    vegan = models.BooleanField(default=False)
    nut_allergy = models.BooleanField(default=False)
    egg_allergy = models.BooleanField(default=False)
    dairy_allergy = models.BooleanField(default=False)
    soy_allergy = models.BooleanField(default=False)
    shellfish_allergy = models.BooleanField(default=False)
    fish_allergy = models.BooleanField(default=False)

    notes = models.CharField(max_length=300, blank=True)



class Survey (models.Model):

    title = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    isClose = models.BooleanField(default=False)


class SurveyParticipation (models.Model):

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    participant = models.ForeignKey(InvolvedEvent, on_delete=models.CASCADE)


class OptionInSurvey (models.Model):
    name = models.CharField(max_length=50,default="option1")
    description = models.CharField(max_length=100,default="option1")
    survey = models.ForeignKey(Survey,on_delete=models.CASCADE) #many options to one survey



class UserChoose(models.Model):

    participation = models.ForeignKey(InvolvedEvent,on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey,on_delete=models.CASCADE)
    choice = models.ForeignKey(OptionInSurvey,on_delete=models.CASCADE)
