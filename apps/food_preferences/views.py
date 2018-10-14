from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy

from apps.food_preferences.models import FoodPreferences
from apps.food_preferences.forms import FoodPreferencesForm

class UpdateFoodPreferencesView(generic.View):

    model = FoodPreferences
    success_url = reverse_lazy('user_profile')


    def post(self, request, *args, **kwargs):

        old, _ = FoodPreferences.objects.filter(user=request.user).delete()

        form = FoodPreferencesForm(request.POST)
        prefs = form.save(commit=False)
        prefs.user = request.user
        prefs.save()
        return redirect(self.success_url)
