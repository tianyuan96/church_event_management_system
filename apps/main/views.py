from django.shortcuts import render
from django.views import generic


class HomeView(generic.TemplateView):
    template_name = 'index.html'
    
class ChooseMealView(generic.TemplateView):
    template_name = 'choose_meal.html'
