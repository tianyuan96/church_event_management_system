from django.shortcuts import render
from django.views import generic
from .forms import EventCreationForm
from . import models
from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Event
from django.urls import reverse_lazy
from django.http import Http404, HttpResponseRedirect


class EventView(generic.View):

    template_name = "event_detail.html"
    form_class = EventCreationForm

    def get(self, request, *args, **kwargs):

        return render(request,self.template_name)


class CreateEventView(CreateView):

    template_name = "create_event2.html"
    orgProfile = "org_account/org_profile.html"#ganization_profile
    form_class = EventCreationForm
    title = 'Create Event'



    def get(self, request, *args, **kwargs):
        user = request.user
        if user is not None:
            if user.is_active:
                form =  self.form_class
                return render(request,self.template_name,{"form":form})
        return render(request,"event_detail.html", {"event": user, 'errors': ""})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            location = form.cleaned_data['location']
            date = form.cleaned_data['date']
            description = form.cleaned_data['description']

            newEvent = Event(name=name, location=location,
                             date = date,description = description,
                             host=user)
            newEvent.save() #save it to the database

            return HttpResponseRedirect('/accounts/organisations/profile')

        return render(request,"event_detail.html", {"event": form, 'errors': form.errors})


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
