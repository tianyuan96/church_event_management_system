from django.shortcuts import render
from django.views import generic
from apps.events.models import Event


class SitemapView(generic.TemplateView):
    template_name = 'sitemap.html'


class HomeView(generic.TemplateView):
    template_name = 'index.html'

    def get(self,request,*args,**kwargs):
        all_event = Event.objects.all()
        context = {
            "events": all_event,
        }
        return render(request,self.template_name,context=context)


class EventDetailView(generic.TemplateView):
    template_name = 'event_detail.html'


class ChooseMealView(generic.TemplateView):
    template_name = 'choose_meal.html'


class ChooseMealSuccessView(generic.TemplateView):
    template_name = 'choose_meal_success.html'


class EventPlannerView(generic.TemplateView):
    template_name = 'event_planner.html'


class CreateEventView(generic.TemplateView):
    template_name = 'create_event.html'


class CaterView(generic.TemplateView):
    template_name = 'cater.html'


class EventOfferView(generic.TemplateView):
    template_name = 'event_offer.html'
