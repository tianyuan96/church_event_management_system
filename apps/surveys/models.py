from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class FoodPreferences(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One user has one set of food prefs

    vegetarian = models.BooleanField()
    vegan = models.BooleanField()
    nut_allergy = models.BooleanField()
    egg_allergy = models.BooleanField()
    dairy_allergy = models.BooleanField()
    soy_allergy = models.BooleanField()
    shellfish_allergy = models.BooleanField()
    fish_allergy = models.BooleanField()

    notes = models.CharField(max_length=300, blank=True)
