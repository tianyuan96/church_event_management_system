from django import forms

from apps.food_preferences.models import FoodPreferences
# Create your views here.
class FoodPreferencesForm(forms.ModelForm):

    class Meta:

        model = FoodPreferences
        exclude = ('user', )
