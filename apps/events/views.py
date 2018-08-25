from django.shortcuts import render
from django.views import generic
from .forms import EventCreationForm


class EventView(generic.FormView):

    form_class = EventCreationForm
