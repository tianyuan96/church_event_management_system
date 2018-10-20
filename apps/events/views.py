from django.shortcuts import render
from django.views import generic
from .forms import EventCreationForm, EventUpdateForm, Event, PostCreationForm, PostUpdateForm, ReplyCreationForm
from . import models
from django.shortcuts import render, redirect,reverse
from django.views.generic import edit
from .models import Event, InvolvedEvent, Post, ReplyTo, PostLike
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404, HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from apps.surveys.models import Survey
from apps.core import views as core_views
from django.contrib.auth.decorators import login_required
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver

from utils.mail.mail_server import ForumReplyEmail, PostUpdateEmail

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
    login_url = reverse_lazy('org_accounts:login')  # If the user isn't logged in, they will be redirected here (see: LoginRequiredMixin)

    def form(self):
        form = self.form_class()
        form['host'].initial = self.request.user.id
        return form



class EventDetailsView(LoginRequiredMixin, generic.DetailView, core_views.BaseView):

    model = Event
    context_object_name = 'event'
    template_name = 'event_detail.html'
    page_title = 'Choose My Meal'
    login_url = reverse_lazy("user_accounts:login")

    def surveys(self):
        event = self.object
        return Survey.objects.filter(event=event)

    def has_joined(self):
        event = self.object
        user = self.request.user
        return InvolvedEvent.objects.filter(participant=user, event=event).exists()

    def number_of_participant(self):
        event = self.object
        return  InvolvedEvent.objects.filter(event=event).count()



class DeleteEventView(generic.DeleteView):

    model = Event
    success_url = reverse_lazy('org_accounts:profile')

    def get_success_url(self):
        return self.success_url

class UpdateEventView(edit.UpdateView, core_views.BaseView):

    model = Event
    template_name = "event_update.html"
    page_title = "Update Event"
    form_class = EventUpdateForm
    success_url = reverse_lazy('org_accounts:profile')



class CreateSuccessView(generic.TemplateView, core_views.BaseView):

    template_name = 'event_success.html'
    page_title = "Success"


# Shows the post on the page
class DiscussionView(generic.CreateView, core_views.BaseView):
    template_name = "create_post.html"
    form_class = PostCreationForm
    page_title = "Discussion"
    def get(self, request, eventId):

        event = Event.objects.get(id=eventId)

        form=self.form_class
        context = {
            "event": event,
            "form":form,
        }
        return render(request, self.template_name, context=context)

class DeletePostView(generic.DeleteView):

    model = Post

    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        user = request.user
        if Post.objects.filter(author=user,id=pk).exists():
            return super(DeletePostView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

    def get_success_url(self, **kwargs):

        return reverse_lazy("event_forums", args=(self.object.eventID.id,))

class UpdatePostView(generic.UpdateView, core_views.BaseView):

    model = Post
    template_name = "post_update_form.html"
    form_class = PostUpdateForm

    def get_success_url(self, **kwargs):

        return reverse_lazy("event_forums", args=(self.object.eventID.id,))

    """
        This function runs whenever a post is created, updated, or deleted
    """
    @receiver(pre_save, sender=Post)
    def on_update(**kwargs):
        # print(kwargs)
        post = kwargs['instance']
        if not post.id:  # If the post is being created, it will be none here (I don't know why)
            # print('Post Created')
            return

        print("Just updated Post: {}".format(post))
        likes = PostLike.objects.filter(postID=post)

        email_list = []
        for like in likes:
            email_list += [like.author.email]

        post_update_email = PostUpdateEmail()
        post_update_email.send(email_list, post.id)


# Sets up the posts in the database
class PostCreationView(LoginRequiredMixin, generic.DetailView, generic.CreateView, core_views.BaseView):

    template_name = "create_post.html"
    form_class = PostCreationForm
    model = Event
    context_object_name = "event"

    login_url = reverse_lazy("user_accounts:login")

    def form(self):
        form = self.form_class()
        return form

    def posts(self):
        event = self.object
        return Post.objects.filter(eventID=event, type=0).order_by('-date')

    def replies(self):
        event = self.object
        return Post.objects.filter(eventID=event, type=1).order_by('date')

    def reply_to(self):
        event = self.object
        return ReplyTo.objects.filter(eventID=event)

    def reply_form(self):
        return ReplyCreationForm

    def has_liked(self):
        event = self.object
        user = self.request.user
        return[ post_like.postID.id for post_like in PostLike.objects.filter(eventID=event, author=user)]


    def has_joined(self):
        event = self.object
        user = self.request.user
        return InvolvedEvent.objects.filter(participant=user, event=event).exists()


    def post(self, request, *args, **kwargs):
        user = request.user
        eventID = kwargs.get("pk")
        if user is not None:
            if user.is_active:
                form = self.form_class(request.POST.copy(), request.FILES)
                if form.is_valid():
                    self.object = form.save(commit=False)
                    self.object.author = user
                    self.object.eventID = Event.objects.get(id=eventID)
                    self.object.date = datetime.datetime.now()
                    self.object.type = 0
                    self.object.save()
                    return HttpResponseRedirect('/event/discussion/'+str(eventID))
                else:
                    print(form.errors)
                    return HttpResponseRedirect(request.path_info)

        return HttpResponseRedirect('/')


class ReplyCreationView(generic.CreateView):

    template_name = "create_post.html"
    form_class = ReplyCreationForm
    model = Post

    def get(self, request, eventID, postID):
        user = request.user
        #eventID = request.POST.get("event", "")
        event = Event.objects.get(id=eventID)
        post = Post.objects.get(id=postID)
        form = PostCreationForm
        if user is not None:
            if user.is_active:
                reply_form = self.form_class
                posts = Post.objects.filter(eventID=eventID, type=0).order_by('-date')
                replies = Post.objects.filter(eventID=event, type=1).order_by('date')
                reply_to = ReplyTo.objects.filter(eventID=event).order_by('date')
                context = {
                    "event": event,
                    "posts": posts,
                    "form": form,
                    "reply_form": reply_form,
                    "replies": replies,
                    "reply_to": reply_to,

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
                    self.object = Post()
                    self.object.message = message
                    self.object.author = user
                    self.object.eventID = Event.objects.get(id=eventID)
                    self.object.date = datetime.datetime.now()
                    self.object.type = 1
                    self.object.save()

                    replyID = self.object.id
                    record = ReplyTo()
                    record.eventID = Event.objects.get(id=eventID)
                    record.author = Post.objects.get(id=postID)
                    record.replier = Post.objects.get(id=replyID)
                    record.postID = Post.objects.get(id=postID)
                    record.save()

                    # Notify the toplevel person someone has replied to their post
                    email = Post.objects.get(id=postID).author.email
                    print('HERE:', email)
                    forum_reply_email = ForumReplyEmail()
                    forum_reply_email.send(email, eventID)

                    return HttpResponseRedirect('/event/discussion/'+eventID)
                else:

                    return HttpResponseRedirect(request.path_info)

        return HttpResponseRedirect('/')


class ReplyToCommentView(generic.CreateView):
    template_name = "create_post.html"
    form_class = ReplyCreationForm
    model = Post

    def get(self, request, eventID, postID):
        user = request.user
        #eventID = request.POST.get("event", "")
        event = Event.objects.get(id=eventID)
        post = Post.objects.get(id=postID)
        form = PostCreationForm
        if user is not None:
            if user.is_active:
                reply_form = self.form_class
                posts = Post.objects.filter(eventID=eventID, type=0).order_by('-date')
                replies = Post.objects.filter(eventID=event, type=1).order_by('date')
                reply_to = ReplyTo.objects.filter(eventID=event).order_by('date')
                context = {
                    "event": event,
                    "posts": posts,
                    "form": form,
                    "reply_form": reply_form,
                    "replies": replies,
                    "reply_to": reply_to,

                }
                return render(request, self.template_name, context=context)
        return HttpResponseRedirect('/')




    def post(self, request, *args, **kwargs):
        user = request.user
        eventID = kwargs.get("eventID")
        postID = kwargs.get("postID")
        commentID = kwargs.get("commentID")
        if user is not None:
            if user.is_active:
                message = request.POST['message']
                #form = self.form_class(request.POST.copy(), request.FILES)
                #if form.is_valid():
                if message is not None:

                    #self.object = form.save(commit=False)
                    self.object = Post()
                    self.object.message = message
                    self.object.author = user
                    self.object.eventID = Event.objects.get(id=eventID)
                    self.object.date = datetime.datetime.now()
                    self.object.type = 1
                    self.object.save()

                    replyID = self.object.id
                    record = ReplyTo()
                    record.eventID = Event.objects.get(id=eventID)
                    record.author = Post.objects.get(id=commentID)
                    record.replier = Post.objects.get(id=replyID)
                    record.postID = Post.objects.get(id=postID)
                    record.save()

                    return HttpResponseRedirect('/event/discussion/'+eventID)
                else:

                    return HttpResponseRedirect(request.path_info)

        return HttpResponseRedirect('/')

class PostLikeView(generic.View):
    template_name = "create_post.html"
    model = PostLike

    form_class = PostCreationForm
    #success_url = reverse_lazy('/event/discussion/'+eventID)
    def get(self, request, eventID, postID):
        user = request.user
        #eventID = request.POST.get("event", "")
        event = Event.objects.get(id=eventID)
        post = Post.objects.get(id=postID)
        form = PostCreationForm
        if user is not None:
            if user.is_active:
                post = Post.objects.get(id=postID)
                event = Event.objects.get(id=eventID)

                post_like = PostLike.objects.filter(eventID=event, postID=post, author=user).count()
                if post_like == 0:
                    self.object = PostLike()
                    self.object.author = user

                    post = Post.objects.get(id=postID)
                    post.likes += 1
                    post.save()
                    self.object.postID = post
                    self.object.eventID = event
                    self.object.save()
                return HttpResponseRedirect('/event/discussion/'+eventID)
        return HttpResponseRedirect('/')


class PostUnlikeView(generic.DeleteView):
    model=PostLike
    def delete(self, request, *args, **kwargs):
        try:
            event=Event.objects.get(id=kwargs["eventID"])
            post=Post.objects.get(id=kwargs["postID"])
            post_like=self.model.objects.get(author=request.user,eventID=event,postID=post)

            post_like.delete()
            post.likes-=1
            post.save()
            return redirect('event_forums', pk=event.id)
        except:
            return Http404
