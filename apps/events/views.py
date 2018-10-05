from django.shortcuts import render
from django.views import generic
from .forms import EventCreationForm, EventUpdateForm, Event, PostCreationForm, PostUpdateForm, ReplyCreationForm
from . import models
from django.shortcuts import render, redirect
from django.views.generic import edit
from .models import Event, InvolvedEvent, Post, Reply
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from apps.surveys.models import Survey
from apps.core import views as core_views
import datetime



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


class EventDetailsView(generic.DetailView, core_views.BaseView):

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


# Shows the post on the page
class DiscussionView(generic.CreateView, core_views.BaseView):
    template_name = "create_post.html"
    form_class = PostCreationForm
    page_title = "TEST"
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


class UpdatePostView(generic.UpdateView):
    model = Post
    template_name = "post_update_form.html"
    form_class = PostUpdateForm
    def get_success_url(self, **kwargs):


        return reverse_lazy("event_forums", args=(self.object.eventID.id,))

# Sets up the posts in the database
class PostCreationView(LoginRequiredMixin, generic.DetailView, core_views.BaseView):

    template_name = "create_post.html"
    form_class = PostCreationForm
    model = Event
    context_object_name = "event"
    page_title = "TEST 2"


#    def get(self, request, *args, **kwargs):
#        user = request.user
#       # event = Event.objects.get(id=eventID)
#        if user is not None:
#            if user.is_active:
#                form = self.form_class

#                return render(request, self.template_name, {"form": form})
 #       return HttpResponseRedirect('/')


    # def event(self):
    #     event = self.object
    #     return event
        # return Event.objects.get(id=self.request.GET['eventID'])

    def form(self):
        return self.form_class

    def posts(self):
        event = self.object
        return Post.objects.filter(eventID=event).order_by('-date')

    def replies(self):
        event = self.object
        return Reply.objects.filter(eventID=event).order_by('date')

    def reply_form(self):
        return ReplyCreationForm


    # def post(self, request, *args, **kwargs):
    #     user = request.user
    #     eventID = kwargs.get("eventID")
    #     if user is not None:
    #         if user.is_active:
    #             form = self.form_class(request.POST.copy(), request.FILES)
    #             if form.is_valid():
    #                 self.object = form.save(commit=False)
    #                 self.object.author = user
    #                 self.object.eventID = Event.objects.get(id=eventID)
    #                 self.object.date = datetime.datetime.now()
    #                 self.object.save()
    #                 return HttpResponseRedirect('/event/discussion/'+eventID)
    #             else:
    #                 print(form.errors)
    #                 return HttpResponseRedirect(request.path_info)

    #     return HttpResponseRedirect('/')


class ReplyCreationView(generic.CreateView):
    template_name = "create_post.html"
    form_class = ReplyCreationForm
    model = Reply





    def get(self, request, eventID, postID):
        user = request.user
        #eventID = request.POST.get("event", "")
        event = Event.objects.get(id=eventID)
        post = Post.objects.get(id=postID)
        form = PostCreationForm
        if user is not None:
            if user.is_active:
                reply_form = self.form_class
                posts = Post.objects.filter(eventID=eventID).order_by('-date')
                replies = Reply.objects.filter(eventID=eventID).order_by('date')
                context = {
                    "event": event,
                    "posts": posts,
                    "form": form,
                    "reply_form": reply_form,
                    "replies": replies

                }
                return render(request, self.template_name, context=context)
        return HttpResponseRedirect('/')




    def post(self, request, *args, **kwargs):
        user = request.user
        eventID = kwargs.get("eventID")
        postID = kwargs.get("postID")
        if user is not None:
            if user.is_active:
                message = request.POST['message']
                #form = self.form_class(request.POST.copy(), request.FILES)
                #if form.is_valid():
                if message is not None:

                    #self.object = form.save(commit=False)
                    self.object = Reply()
                    self.object.message = message
                    self.object.author = user
                    self.object.eventID = Event.objects.get(id=eventID)
                    self.object.postID = Post.objects.get(id=postID)
                    self.object.date = datetime.datetime.now()
                    self.object.save()
                    return HttpResponseRedirect('/event/discussion/'+eventID)
                else:

                    return HttpResponseRedirect(request.path_info)

        return HttpResponseRedirect('/')
