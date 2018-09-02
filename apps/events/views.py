from django.shortcuts import render
from django.views import generic
from .forms import EventCreationForm
from . import models
from django.shortcuts import render
from django.urls import reverse_lazy


class EventView(generic.FormView):

    template_name = "main/create_event.html"
    form_class = EventCreationForm



class ModifyEventView(generic.View):

    successful_url = reverse_lazy('successfully_modified')

    def get(self, request, *args, **kwargs):
        event = models.Event.objects.get(id=id)

        event.name = request.GET.get('name')
        event.date = request.GET.get('date')
        event.location = request.GET.get('venue')
        event.description = request.GET.get('description')
        event.save()
        return render(request, self.template_name, {'user': request.user, 'title': request.user.email})

