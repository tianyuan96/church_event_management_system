from django.shortcuts import render
from django.views import generic
from .forms import EventCreationForm
from . import models
from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Event
from django.urls import reverse_lazy
from django.http import Http404

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


class DeleteEventView(generic.DeleteView):

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(DeleteEventView, self).get_object()
        if not obj.owner == self.request.user:
            raise Http404
        return obj




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
