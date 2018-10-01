from django.shortcuts import render
from django.views import generic
from .forms import EventCreationForm, EventUpdateForm, Event
from . import models
from django.shortcuts import render, redirect
from django.views.generic import edit
from .models import Event,InvolvedEvent
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from apps.surveys.models import Survey
from apps.core import views as core_views

class JoinEvent(generic.View):
    #success_url =

    def post(self,request, *args, **kwargs):
        user = request.user
        event_id = request.POST.get("event", "")
        event = Event.objects.get(id=event_id)
        operation = request.POST.get("operation", "")
        if user is not None and not user.is_anonymous:
            if user.is_active and event:
                if operation == "Join":
                    self.joinEvent(user, event)
                elif operation == "unJoin":
                    self.unJoinEnvent(user, event)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


    def joinEvent(self, user, event):

        join = InvolvedEvent(participant=user, event=event)
        join.save()

    def unJoinEnvent(self, user, event):
        involvedEvent = InvolvedEvent.objects.filter(event=event, participant=user)
        involvedEvent.all().delete()


class CreateEventView(LoginRequiredMixin, generic.CreateView, core_views.BaseView):

    template_name = "create_event.html"
    form_class = EventCreationForm
    model = Event
    page_title = 'Create Event'
    success_url = reverse_lazy('home')
    login_url = '/accounts/organisations/login/'  # If the user isn't logged in, they will be redirected here (see: LoginRequiredMixin)

    def form(self):
        form = self.form_class()
        form['host'].initial = self.request.user.id
        return form


class EventDetailView(generic.DetailView, core_views.BaseView):

    model = Event
    context_object_name = 'event'
    template_name = 'event_detail.html'
    page_title = 'Choose My Meal'

    def surveys(self):
        event = self.object
        return Survey.objects.filter(event=event)

    def has_joined(self):
        event = self.object
        user = self.request.user
        return InvolvedEvent.objects.filter(participant=user, event=event).exists()


class DeleteEventView(generic.DeleteView):

    model = Event
    success_url = reverse_lazy('org_profile')


class UpdateEventView(edit.UpdateView):

    model = Event
    template_name = "event_update.html"
    form_class = EventUpdateForm
    success_url = reverse_lazy('org_profile')


class CreateSuccessView(generic.TemplateView, core_views.BaseView):

    template_name = 'event_success.html'
    page_title = "Success"
