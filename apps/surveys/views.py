from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from django.views import generic
from .forms import CreateSurveyForm
from .models import Survey,OptionInSurvey,SurveyParticipation,UserChoose
from apps.events.models import Event,InvolvedEvent
import json
# Create your views here.


class CreateSurveyView(generic.View):
    template_name = 'event_offer.html'
    form_class = CreateSurveyForm
    model = Survey
    success_url = '/thanks/'
    title = 'Create Survey'

    def get(self, request,eventId):
        event=Event.objects.get(id=eventId)
        context={
            "event":event,
            "surveys":Survey.objects.all(),
        }
        return render(request, self.template_name, context=context)

class SubmitSurveyView(generic.View):
    def post(self, request):
        optionId = self.request.POST.get("option", "")
        try:
            option=OptionInSurvey.objects.get(id=int(optionId))
            survey=Survey.objects.get(id=option.survey.id)
            print("--------------------------")
            print(survey)
            print(request.user)
            surveyParticipation =SurveyParticipation()
            surveyParticipation.survey=survey
            surveyParticipation.participant=self.request.user
            surveyParticipation.save()

            userchoose=UserChoose()
            userchoose.choice=option
            userchoose.user=self.request.user
            userchoose.save()

        except():
            pass
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

class DoSurveyView(generic.View):
    template_name = 'do_survey.html'
    def get(self, request,surveyId):
        survey=Survey.objects.get(id=surveyId)
        options = OptionInSurvey.objects.filter(survey=survey)
        context={
            "survey":survey,
            "options":options,
        }
        return render(request, self.template_name, context=context)


class DeleteSurveyView(generic.View):
    def post(self, request):
        surveyId = self.request.POST.get("surveyId", "")
        try:
            Survey.objects.get(id=int(surveyId)).delete()
        except():
            pass
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



class SeeSurveyResultView(generic.View):
    template_name = 'view_survey_result.html'

    def get(self, request,surveyId):
        summary=self._construct_result(surveyId)
        survey = Survey.objects.get(id=surveyId)
        options = OptionInSurvey.objects.filter(survey=survey)
        context={
            "survey":survey,
            "options":options,
            "summary":summary,
            "chart_data":self._construct_json_result(surveyId)
        }
        return render(request, self.template_name, context=context)



    def _construct_result(self,surveyId):
        summary=dict()
        survey = Survey.objects.get(id=surveyId)
        options = OptionInSurvey.objects.filter(survey=survey)
        numTotalParticipant=InvolvedEvent.objects.filter(eventId=survey.event).count()
        summary["total"]=numTotalParticipant
        for option in options:
            numChoice=UserChoose.objects.filter(choice=option).count()#get number for people who choose this option
            summary[""+str(option.id)]=numChoice
        return summary

    def _construct_json_result(self, surveyId):
        result=[]
        survey = Survey.objects.get(id=surveyId)
        options = OptionInSurvey.objects.filter(survey=survey)
        for option in options:
            numChoice=UserChoose.objects.filter(choice=option).count()#get number for people who choose this option
            result.append([option.name,numChoice])
        return json.dumps(result)



class ProcessSurvey(generic.View):
    template_name = 'event_offer.html'
    model = Survey
    def post(self,request):
        title = request.POST.get("title","")
        eventId = self.request.POST.get("event", "")
        survey = self.model()
        survey.title = title
        survey.event = Event.objects.get(id=int(eventId))
        survey.owner = self.request.user
        error=""
        try:
            survey.save()
        except():
            error = "invalid input"

        choiceList=request.POST.getlist("choiceList[]")
        if(self._check_valid_choice_list(choiceList)):
            options = self._create_choice_model_list(choiceList)
            for option in options:
                option.survey = survey
                option.save()
        return render(request, self.template_name, {'error': error ,  "event":Event.objects.get(id=int(eventId)),})


    def _check_valid_choice_list(self,choiceList):
        if len(choiceList)%2==0:
            return True
        else:
            return False

    def _create_choice_model_list(self,choiceList):
        i=0
        results=[]
        while i< len(choiceList):
            option=OptionInSurvey()
            option.name=choiceList[i]
            option.description = choiceList[i+1]
            results.append(option)
            i+=2
        return results





