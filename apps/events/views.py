from django.shortcuts import render
from django.views import generic
from .forms import EventCreationForm, EventUpdateForm, Event, PostCreationForm, PostUpdateForm
from . import models
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView
from .models import Event,InvolvedEvent,Post
from django.urls import reverse_lazy
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
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



class JoinEvent(generic.View):
    #success_url =

    def post(self,request, *args, **kwargs):
        user = request.user
        eventId= request.POST.get("event", "")
        operation =request.POST.get("operation", "")
        if user is not None:
            if user.is_active and eventId:
                if operation == "Join":
                    joinEvent(user,eventId)
                elif operation == "unJoin":
                    unJoinEnvent(user, eventId)
                return HttpResponseRedirect("/")



class EventView(generic.View):

    template_name = "event_detail.html"
    form_class = EventCreationForm

    def get(self, request, eventId):
        event = Event.objects.get(id=eventId)
        context={
            "event" : event
        }
        return render(request,self.template_name,context=context)




class CreateEventView(CreateView):

    template_name = "create_event2.html"
    orgProfile = "org_account/org_profile.html"#ganization_profile
    form_class = EventCreationForm
    title = 'Create Event'

    def get(self, request, *args, **kwargs):
        user = request.user
        if user is not None and user.is_staff:
            if user.is_active:
                form =  self.form_class
                return render(request,self.template_name,{"form":form})
        return HttpResponseRedirect('/')

    def post(self, request, *args, **kwargs):
        user = request.user
        if user is not None and user.is_staff:
            form = self.form_class(request.POST.copy(),request.FILES)
            form.data['host'] = user.id
            if form.is_valid():
                form.save() #save it to the database
                return HttpResponseRedirect('/accounts/organisations/profile')
            else:
                print(form.errors)
                return HttpResponseRedirect(request.path_info)


        return HttpResponseRedirect('/')



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
                    return HttpResponseRedirect('/')
                else:
                    print(form.errors)
                    return HttpResponseRedirect(request.path_info)

        return HttpResponseRedirect('/')
