from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages

from apps.food_preferences.models import FoodPreferences
from apps.food_preferences.forms import FoodPreferencesForm

class UpdateFoodPreferencesView(generic.View):

    success_url = reverse_lazy('user_accounts:user_profile')

    def post(self, request, *args, **kwargs):

        # Delete the old user's food prefs
        FoodPreferences.objects.filter(user=request.user).delete()

        # Get the form data and save it to the database as the user's new food prefs
        form = FoodPreferencesForm(request.POST)
        prefs = form.save(commit=False)
        prefs.user = request.user
        prefs.save()
        messages.add_message(request, messages.INFO, 'Successfully updated your food preferences!', extra_tags='success food_preferences')

        return redirect(self.success_url)
