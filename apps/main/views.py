from django.shortcuts import render
from django.views import generic
from apps.events.models import Event, InvolvedEvent
import apps.core.views as core_views
import datetime


class HomeView(generic.TemplateView, core_views.BaseView):

    template_name = 'index.html'
    page_title = "Home"

    def events(self):
        today = datetime.date.today()
        next_week = datetime.date.today() + datetime.timedelta(days=7)
        events = Event.objects.filter(date__range=(today, next_week))

        return events

    def future_events(self):
        next_week = datetime.date.today() + datetime.timedelta(days=7)
        upcoming_events = Event.objects.filter(date__gte=next_week)
        return upcoming_events

    def attending(self):
        user = self.request.user
        attending = InvolvedEvent.objects.filter(participant=user.id)
        return [involvedEvent.event.id for involvedEvent in attending]



class SitemapView(generic.TemplateView, core_views.BaseView):
    template_name = 'sitemap.html'
    page_title = "SiteMap"

# TODO: I think these views should be moved to different apps
class SuccessView(generic.TemplateView, core_views.BaseView):
    template_name = 'survey_response.html'
    page_title = 'Success!'

class ChooseMealView(generic.TemplateView, core_views.BaseView):
    template_name = 'choose_meal.html'
    page_title = 'Meal'


# TODO: What is everything below here? Do we need it???
# class EventDetailView(generic.TemplateView, core_views.TitleView):
#     template_name = 'event_detail.html'
#     page_title = "Event"
#
#
#     def events(self):
#         events = Events.objects.get(id=)
#     def get(self, request, *args, **kwargs):
#
#         Event.objects.filter(id=eventId)
#         context = {
#             "events": all_event,
#         }
#         return render(request, self.template_name, context=context)
#
#

#
#
#
#
# class EventPlannerView(generic.TemplateView):
#     template_name = 'event_planner.html'
#
#
# class CreateEventView(generic.TemplateView):
#     template_name = 'create_event.html'
#
#
# class CaterView(generic.TemplateView):
#     template_name = 'cater.html'
#
#
# class EventOfferView(generic.TemplateView):
#     template_name = '../surveys/templates/event_offer.html'
