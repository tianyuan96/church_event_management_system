from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.shortcuts import redirect, reverse
from django.views import generic
from .forms import CreateSurveyForm
from .models import Survey,OptionInSurvey,SurveyParticipation,UserChoose
from apps.events.models import Event,InvolvedEvent
import json
import datetime
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
        user=request.user
        context = {
            'redirect': reverse('home'),
        }
        if not user.is_anonymous and optionId!= "":
           # try:
            option=OptionInSurvey.objects.get(id=int(optionId))
            survey=Survey.objects.get(id=option.survey.id)
            context["title"]= survey.title
            context["isSuccess"] = True


            if self.isUserParticipatedEvent(user,survey.event):

                participation = InvolvedEvent.objects.get(participant=request.user, eventId=survey.event)
                if self.isUserParticipatedSurvey(participation,survey):
                    # user has participated this survey before
                    self.updateChoice(participation,survey,option)
                    context["message"] ="successfully update your choice"
                    return render(request, "survey_response.html", context=context)
                else:
                    #create new result record for the survey
                    self.createNewChoiceRecord(survey,option,user,participation)
                    context["message"]="successfully submit your choice"
                    return render(request, "survey_response.html", context=context)

            else:
                #the user is not in this event
                context["isSuccess"]=False
                context["message"] = "you have not join this event yet"
                return render(request, "survey_response.html", context=context)


        else:
            context["message"] = "you should login before submit a anything"
            if optionId == "":
                context["message"] = "you should choose a option before submit"
            return render(request, "survey_response.html", context=context)

    def createNewChoiceRecord(self,survey,option,user,participation):
        surveyParticipation = SurveyParticipation()
        surveyParticipation.survey = survey
        surveyParticipation.participant = participation
        surveyParticipation.save()

        userchoose = UserChoose()
        userchoose.choice = option
        userchoose.participation = participation
        userchoose.survey = survey
        userchoose.save()

    def isUserParticipatedEvent(self,user,event):
        if InvolvedEvent.objects.filter(participant=user, eventId=event).count()>0:
            return True
        return False

    def isUserParticipatedSurvey(self,participation,survey):
        if SurveyParticipation.objects.filter(participant =participation,survey=survey).count()>0:
            return True
        return False

    def updateChoice(self, participation,survey,option):
        userchoose = UserChoose.objects.get(participation=participation,survey=survey,)
        userchoose.choice=option
        userchoose.save()


class DoSurveyView(generic.View):
    template_name = 'do_survey.html'
    success_template = 'survey_response.html'
    def get(self, request,surveyId):
        try:
            survey=Survey.objects.get(id=surveyId)
            event=Event.objects.get(id=survey.event.id)
            if datetime.date.today() > event.date:
                survey.isClose=True
                survey.save()
                return render(request, self.success_template, context=self.generateFailContext(request,event))
            options = OptionInSurvey.objects.filter(survey=survey)
            context={
                "survey":survey,
                "options":options,
            }
            return render(request, self.template_name, context=context)
        except:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    def generateFailContext(self,request,event):
        return {
            "isSuccess": False,
            "event": event,
            "redirect": reverse("event-datail",kwargs={"eventId",event.id}),
            "message": "the survey has been closed",
        }


class DeleteSurveyView(generic.View):

    def post(self, request):
        surveyId = self.request.POST.get("surveyId", "")
        try:
            Survey.objects.get(id=int(surveyId)).delete()
        except():
            pass
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

class CloseSurveyView(generic.View):

    def post(self, request):
        surveyId = self.request.POST.get("surveyId", "")
        try:
            survey = Survey.objects.get(id=int(surveyId))
            if(survey.isClose):
                survey.isClose =False
            else:
                survey.isClose = True
            survey.save()
        except():
            pass
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

class SeeSurveyResultView(generic.View):
    template_name = 'view_survey_result.html'

    def get(self, request,surveyId):
        summary=self._construct_result(surveyId)
        survey = Survey.objects.get(id=surveyId)
        options = OptionInSurvey.objects.filter(survey=survey)
        sumOfChoosen = 0;
        context={
            "survey":survey,
            "options":options,
            "summary":summary,
            "chart_data":self._construct_json_result(surveyId,sumOfChoosen),
            "sumOfChoosen":sumOfChoosen
        }
        return render(request, self.template_name, context=context)



    def _construct_result(self,surveyId):
        summary=dict()
        survey = Survey.objects.get(id=surveyId)
        options = OptionInSurvey.objects.filter(survey=survey)
        numTotalParticipant=InvolvedEvent.objects.filter(eventId=survey.event).count()
        summary["total"]=numTotalParticipant
        for option in options:
            numChoice=UserChoose.objects.filter(choice=option,survey=survey).count()#get number for people who choose this option
            summary[""+str(option.id)]=numChoice
        return summary

    def _construct_json_result(self, surveyId,sumOfChoosen):
        result=[]
        survey = Survey.objects.get(id=surveyId)
        options = OptionInSurvey.objects.filter(survey=survey)
        sumOfChoosen = 0
        for option in options:
            numChoice=UserChoose.objects.filter(choice=option,survey=survey).count()#get number for people who choose this option
            result.append([option.name,numChoice])
            sumOfChoosen+=numChoice
        return json.dumps(result)



class ProcessSurvey(generic.View):
    template_name = 'event_offer.html'
    success_template = 'survey_response.html'
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
            survey.full_clean()
            survey.save()
            choiceList = request.POST.getlist("choiceList[]")
            if (self._check_valid_choice_list(choiceList)):
                options = self._create_choice_model_list(choiceList)
                if len(options)>0:
                    for option in options:
                        option.survey = survey
                        try:
                            option.full_clean()
                            option.save()
                        except:

                            # not a valid option
                            error = "please add some choice to a survey"
                            return render(request, self.template_name,
                                          {'error': error, "isSuccess": False, "event": Event.objects.get(
                                              id=int(eventId)), })
            return render(request, self.success_template, self._define_success_context(error,eventId))
        except:
            error = "invalid input"
            return render(request, self.template_name, {'error': error, "isSuccess": False, "event": Event.objects.get(
            id=int(eventId)), })

    def _define_success_context(self,error,eventId):
        return {'error': error,
                "isSuccess": True,
                "event": Event.objects.get(id=int(eventId)),
                "redirect": reverse("event-datail",kwargs={"eventId": eventId}),
                "message": "you have successfully created a survey"
                }



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





class SuccessView(generic.TemplateView):
    template_name = 'survey_response.html'

    def get(self, request, context):
        return render(request, self.template_name, context=context)