from django.shortcuts import render
from django.views import generic
from apps.events.models import Event, InvolvedEvent
import datetime


class SitemapView(generic.TemplateView):
    template_name = 'sitemap.html'


class HomeView(generic.TemplateView):
    template_name = 'index.html'

    def get(self,request,*args,**kwargs):
        user=request.user
        one_week_later_time = (datetime.date.today() + datetime.timedelta(days=7))
        all_event_within_this_week = Event.objects.filter(date__range =(datetime.date.today()- datetime.timedelta(days=7),one_week_later_time))

        all_event_after_this_week = Event.objects.filter(date__gte = one_week_later_time)
        all_joined_event = InvolvedEvent.objects.filter(participant=user.id)
        context = {
            "events": all_event_within_this_week,
            "events_later":all_event_after_this_week,
            "joinedEvent":[ involvedEvent.eventId for involvedEvent in all_joined_event]
        }
        return render(request,self.template_name,context=context)


class EventDetailView(generic.TemplateView):
    template_name = 'event_detail.html'

    def get(self, request, *args, **kwargs):

        Event.objects.filter(id=eventId)
        context = {
            "events": all_event,
        }
        return render(request, self.template_name, context=context)


class ChooseMealView(generic.TemplateView):
    template_name = 'choose_meal.html'



class SuccessView(generic.TemplateView):
    template_name = 'survey_response.html'

    def get(self, request, context):
        return render(request, self.template_name, context=context)


class EventPlannerView(generic.TemplateView):
    template_name = 'event_planner.html'


class CreateEventView(generic.TemplateView):
    template_name = 'create_event.html'


class CaterView(generic.TemplateView):
    template_name = 'cater.html'


class EventOfferView(generic.TemplateView):
    template_name = '../surveys/templates/event_offer.html'
