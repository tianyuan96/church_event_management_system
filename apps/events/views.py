from django.shortcuts import render
from django.views import generic
from .forms import EventCreationForm, EventUpdateForm, Event, PostCreationForm, PostUpdateForm
from . import models
from django.shortcuts import render, redirect
<<<<<<< HEAD
from django.views.generic import edit
from .models import Event,InvolvedEvent
from django.contrib.auth.mixins import LoginRequiredMixin
=======
from django.views.generic.edit import CreateView, UpdateView
from .models import Event,InvolvedEvent,Post
>>>>>>> newForums
from django.urls import reverse_lazy
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
<<<<<<< HEAD
from apps.surveys.models import Survey
from apps.core import views as core_views
=======
import datetime


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


>>>>>>> newForums

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
<<<<<<< HEAD
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
=======
                    unJoinEnvent(user, eventId)
                return HttpResponseRedirect("/")



class EventView(generic.View):
>>>>>>> newForums

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
<<<<<<< HEAD
    template_name = "event_update.html"
=======
    #fields = ['name', 'date', 'location', 'description', 'imageFile']
    #template_name_suffix = '_update_form'

    template_name = "event_update_form.html"
>>>>>>> newForums
    form_class = EventUpdateForm


    success_url = reverse_lazy('org_profile')

#
# class DiscussionView(generic.View):
#     template_name = "event_discussion"
#     form_class = PostCreationForm
#
#     def get(self, request, eventId):
#         event = Event.objects.get(id=eventId)
#         context={
#             "event" : event
#         }
#         return render(request,self.template_name,context=context)


class CreateSuccessView(generic.TemplateView, core_views.BaseView):

<<<<<<< HEAD
    template_name = 'event_success.html'
    page_title = "Success"
=======
"""


# Shows the post on the page
class DiscussionView(CreateView):
    template_name = "create_post.html"
    form_class = PostCreationForm

    def get(self, request, eventId):

        event = Event.objects.get(id=eventId)
        print('HERE:', event)
        form=self.form_class
        context = {
            "event": event,
            "form":form,
        }
        return render(request, self.template_name, context=context)

class DeletePostView(generic.DeleteView):

    model = Post
    def get_success_url(self, **kwargs):


        return reverse_lazy("event_forums", args=(self.object.eventID.id,))


class UpdatePostView(UpdateView):
    model = Post
    template_name = "post_update_form.html"
    form_class = PostUpdateForm
    def get_success_url(self, **kwargs):


        return reverse_lazy("event_forums", args=(self.object.eventID.id,))

# Sets up the posts in the database
class PostCreationView(CreateView):
    template_name = "create_post.html"
    form_class = PostCreationForm
    model=Post
#    def get(self, request, *args, **kwargs):
#        user = request.user
#       # event = Event.objects.get(id=eventID)
#        if user is not None:
#            if user.is_active:
#                form = self.form_class

#                return render(request, self.template_name, {"form": form})
 #       return HttpResponseRedirect('/')
    def get(self, request, eventID, **kwargs):
        user = request.user
        #eventID = request.POST.get("event", "")

        event = Event.objects.get(id=eventID)
        if user is not None:
            if user.is_active:
                form = self.form_class
                posts = Post.objects.filter(eventID=eventID).order_by('-date')
                context = {
                    "event": event,
                    "form": form,
                    "posts": posts
                }
                return render(request, self.template_name, context=context)
        return HttpResponseRedirect('/')




    def post(self, request, *args, **kwargs):
        user = request.user
        eventID = kwargs.get("eventID")
        if user is not None:
            if user.is_active:
                form = self.form_class(request.POST.copy(), request.FILES)
                if form.is_valid():
                    self.object = form.save(commit=False)
                    self.object.author = user
                    self.object.eventID = Event.objects.get(id=eventID)
                    self.object.date = datetime.datetime.now()
                    self.object.save()
                    return HttpResponseRedirect('/event/discussion/'+eventID)
                else:
                    print(form.errors)
                    return HttpResponseRedirect(request.path_info)

        return HttpResponseRedirect('/')
>>>>>>> newForums
