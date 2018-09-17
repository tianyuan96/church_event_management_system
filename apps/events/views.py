from django.shortcuts import render
from django.views import generic
from .forms import EventCreationForm, EventUpdateForm, Event
from . import models
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView
from .models import Event,InvolvedEvent
from django.urls import reverse_lazy
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from apps.surveys.models import Survey



def joinEvent(user,eventId):
    join = InvolvedEvent()
    join.participant = user
    join.eventId = Event.objects.get(id=eventId)
    is_join = InvolvedEvent.objects.filter(eventId=eventId, participant=user.id).exists()
    if not is_join:
        join.save()
def unJoinEnvent(user,eventId):
    involvedEvent = InvolvedEvent.objects.filter(eventId=eventId, participant=user.id)
    involvedEvent.all().delete()



class JoinEvent(generic.View):
    #success_url =

    def post(self,request, *args, **kwargs):
        user = request.user
        eventId= request.POST.get("event", "")
        operation =request.POST.get("operation", "")
        if user is not None and not user.is_anonymous:
            if user.is_active and eventId:
                if operation == "Join":
                    joinEvent(user,eventId)
                elif operation == "unJoin":
                    unJoinEnvent(user, eventId)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))










class EventView(generic.View):

    template_name = "event_detail.html"
    form_class = EventCreationForm

    def get(self, request, eventId):
        event = Event.objects.get(id=eventId)
        surveys = Survey.objects.filter(event=eventId)
        joinedEvent=[]
        if not request.user.is_anonymous:
            all_joined_event = InvolvedEvent.objects.filter(participant=request.user)
            joinedEvent=[involvedEvent.eventId for involvedEvent in all_joined_event]
        context={
            "event" : event,
            "surveys": surveys,
            "joinedEvent": joinedEvent,
        }
        return render(request,self.template_name,context=context)




class CreateEventView(CreateView):

    template_name = "create_event2.html"
    success_templte = "event_response.html"
    orgProfile = "org_account/org_profile.html"#ganization_profile
    form_class = EventCreationForm
    title = 'Create Event'

    def get(self, request, *args, **kwargs):
        user = request.user
        if user is not None and user.is_staff:
            if user.is_active:
                form =  self.form_class
                return render(request,self.template_name,{"form":form})
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    def post(self, request, *args, **kwargs):
        user = request.user
        if user is not None and user.is_staff:
            form = self.form_class(request.POST.copy(),request.FILES)
            form.data['host'] = user.id
            if form.data['date']:
                if form.is_valid():
                    event=form.save() #save it to the database
                    context=self._make_success_context(event)
                    return render(request,self.success_templte,context=context)
                else:
                    print(form.errors)
                    return render(request,self.template_name,{"form",form})


        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    def _make_success_context(self,event):
        return {"message": "you have successfully create event for" + event.name,
                   "title": event.name,
                   "isSuccess": True,
                   "redirect": reverse_lazy("org_profile")
                   }



class DeleteEventView(generic.DeleteView):

    model = Event
    success_url = reverse_lazy('org_profile')



class UpdateEventView(UpdateView):
    model = Event
    #fields = ['name', 'date', 'location', 'description', 'imageFile']
    #template_name_suffix = '_update_form'
    template_name = "event_update_form.html"
    form_class = EventUpdateForm
    success_url = reverse_lazy('org_profile')


    """
    model = Event
    #fields = ['name', 'date', 'location', 'description', 'imageFile']
    template_name = "event_update_form.html"
    form_class = EventUpdateForm
    success_url = reverse_lazy('org_profile')

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)

  def get(self, request, *args, **kwargs):
        event = models.Event.objects.get(id=id)

        event.name = request.GET.get('name')
        event.date = request.GET.get('date')
        event.location = request.GET.get('venue')
        event.description = request.GET.get('description')
        event.save()
        return render(request, self.template_name, {'user': request.user, 'title': request.user.email})



"""
