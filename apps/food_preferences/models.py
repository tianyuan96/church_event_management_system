from django.db import models
from django.contrib.auth.models import User

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
