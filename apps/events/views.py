from django.shortcuts import render
from django.views import generic
from .forms import EventCreationForm
from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Event

class EventView(generic.View):

    template_name = "event_detail.html"
    form_class = EventCreationForm

    def get(self, request, *args, **kwargs):

        return render(request,self.template_name)


class CreateEventView(CreateView):

    template_name = "create_event2.html"
    form_class = EventCreationForm
    title = 'Create Event'

     # def get(self, request, *args, **kwargs):
     #    con
     #    return render(request,self.template_name)





