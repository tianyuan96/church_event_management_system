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
           # image = request.POST.get('event_image',False)
            if form.is_valid():

                form.save() #save it to the database
                return HttpResponseRedirect('/accounts/organisations/profile')
            else:
                print(form.errors)
                return HttpResponseRedirect(request.path_info)
        #if they don't have the permission, do not let them to do anything
        return HttpResponseRedirect(request.path_info)





class DeleteEventView(generic.DeleteView):

    model = Event
    success_url = reverse_lazy('org_profile')



class UpdateEventView(generic.View):

    successful_url = reverse_lazy('successfully_modified')

    def get(self, request, *args, **kwargs):
        event = models.Event.objects.get(id=id)

        event.name = request.GET.get('name')
        event.date = request.GET.get('date')
        event.location = request.GET.get('venue')
        event.description = request.GET.get('description')
        event.save()
        return render(request, self.template_name, {'user': request.user, 'title': request.user.email})
