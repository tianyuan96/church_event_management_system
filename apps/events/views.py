from django.shortcuts import render
from django.views import generic
from .forms import EventCreationForm
from django.shortcuts import render


class EventView(generic.FormView):

    template_name = "main/create_event.html"
    form_class = EventCreationForm

