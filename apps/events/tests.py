from django.test import TestCase
from apps.events.models import Event,InvolvedEvent
from apps.food_preferences.models import FoodPreferences
from django.contrib.auth.models import User
from apps.surveys.views import CreateSurveyView
# Create your tests here.

class foodPreferenceTest (TestCase):
    def setUp(self):
        user = User.objects.create(email='random@gmail.com', password='auise1234', username='random@gmail.com')
        event = Event.objects.create(name="event",description="des",host=user)
        InvolvedEvent.objects.create(participant=user,event=event)
        FoodPreferences.objects.create(user = user,vegan=True,dairy_allergy=True)
    def test(self):
        cv = CreateSurveyView()
        event = Event.objects.get(name="event")
        ls = cv.generateFoodPreferenceList(event)
        self.assertEqual(ls["vegan"], 1)
        self.assertEqual(ls["dairy allergy"], 1)
        self.assertEqual(ls["soy allergy"] ,0)