from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.views.generic.edit import FormView
from django.shortcuts import redirect, reverse
from django.views import generic
from .forms import CreateSurveyForm,CreateOptionForm
from .models import Survey,OptionInSurvey,SurveyParticipation,UserChoose
from apps.events.models import Event,InvolvedEvent
import json
import datetime
from apps.core import views as core_views
from django.views.generic import edit
from django.urls import reverse_lazy
# Create your views here.


class EmptySurveyGenerator(generic.View):
    def get(self,request,eventId):
        user = request.user
        if user is None:
            return reverse_lazy('home')
        if user.is_staff:
            event = Event.objects.get(id=eventId)
            survey = Survey.create(user, event)
            survey.save()
            return HttpResponseRedirect(
                reverse('add_option_for_survey',kwargs={"eventId":int(eventId),"surveyId":int(survey.id)}))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

class CreateSurveyView(edit.CreateView, core_views.BaseView):
    template_name = 'event_offer.html'
    success_template = 'survey_response.html'
    choice_card_template='choice_card.html'
    survey_form_class = CreateSurveyForm
    option_form_class = CreateOptionForm
    model = Survey
    success_url = '/thanks/'
    title = 'Create Survey'

    def get(self, request, *args, **kwargs):
        eventId=kwargs["eventId"]
        survey=Survey.objects.get(id=int(kwargs["surveyId"]))
        user = request.user
        if user is None:
            return reverse_lazy('home')
        if user.is_staff:
            context={
                "optionForm":self.option_form_class(),
                "survey":survey,
                "options":OptionInSurvey.objects.filter(survey=survey)
            }
            return render(request, self.template_name, context=context)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


    def post(self, request, *args, **kwargs):
        user = request.user
        if user is None:
            return reverse_lazy('home')
        if user.is_staff:
            operation = request.POST.get("operation", "")
            print("operation is ",operation)
            surveyId = request.POST.get("survey", "")
            survey = Survey.objects.get(id=surveyId)
            if operation == "add_option":
                form = self.option_form_class(request.POST, request.FILES)

                if form.is_valid():
                    option = form.save(commit=False)

                    if Survey.objects.filter(id= surveyId).count()>0:
                        option.survey=survey
                        option.save()
                        context = {
                            "optionForm": self.option_form_class(),
                            "survey": survey,
                            "options": OptionInSurvey.objects.filter(survey=survey)
                        }
                        return render(request, self.choice_card_template, context=context)
                context = {
                    "optionForm": form,
                    "survey": survey,
                    "options": OptionInSurvey.objects.filter(survey=survey)
                }
                return render(request, self.choice_card_template, context=context)

            elif operation == "create_survey":
                if(OptionInSurvey.objects.filter(survey=survey).count()<1):
                    context = {
                        "surveyForm": self.survey_form_class(),
                        "optionForm": self.option_form_class(),
                        "survey": survey,
                        "error":"More options are needed to form a survey",
                        "options": OptionInSurvey.objects.filter(survey=survey)
                    }
                    return render(request, self.template_name, context=context)
                form = self.survey_form_class(request.POST)
                print("creating survey")
                if form.is_valid():
                    survey.title=request.POST.get("title", "")
                    survey.isFinalized=True
                    survey.save()
                    return render(request, self.success_template, context=self.generateSuccessContext(survey))
                context = {
                    "surveyForm":form,
                    "optionForm": self.option_form_class(),
                    "survey": survey,
                    "options": OptionInSurvey.objects.filter(survey=survey)
                }
                return render(request, self.template_name, context=context)


    def generateSuccessContext(self, survey):
        return {
            "isSuccess": True,
            "event": survey.event,
            "redirect": reverse("event_detail", kwargs={"pk":survey.event.id}),
            "message": "You have successfully created a new survey called "+survey.title,
        }

    def generateFailContext(self, survey):
        return {
            "isSuccess": False,
            "event": survey.event,
            "redirect": reverse("event_detail", kwargs={"pk": survey.event.id}),
            "message": "Create survey fail",
        }

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

                participation = InvolvedEvent.objects.get(participant=request.user, event=survey.event)
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
        if InvolvedEvent.objects.filter(participant=user, event=event).count()>0:
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
            "redirect": reverse("event_detail",kwargs={"pk":event.id}),
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
        print(surveyId)
        summary=self._construct_result(surveyId)
        survey = Survey.objects.get(id=surveyId)
        options = OptionInSurvey.objects.filter(survey=survey)
        sumOfChoosen = 0;
        context={
            "survey":survey,
            "options":options,
            "summary":summary,
            "chart_data":self._construct_json_result(surveyId,sumOfChoosen),
            "sumOfChoosen":self._sum_result(surveyId)
        }

        return render(request, self.template_name, context=context)



    def _construct_result(self,surveyId):
        summary=dict()
        survey = Survey.objects.get(id=surveyId)
        options = OptionInSurvey.objects.filter(survey=survey)
        numTotalParticipant=InvolvedEvent.objects.filter(event=survey.event).count()
        summary["total"]=numTotalParticipant
        for option in options:
            numChoice=UserChoose.objects.filter(choice=option,survey=survey).count()#get number for people who choose this option
            summary[""+str(option.id)]=numChoice
        return summary

    def _construct_json_result(self, surveyId,sumOfChoosen):
        result=[]
        survey = Survey.objects.get(id=surveyId)
        options = OptionInSurvey.objects.filter(survey=survey)
        for option in options:
            numChoice = UserChoose.objects.filter(choice=option,survey=survey).count()#get number for people who choose this option
            result.append([option.name,numChoice])
            sumOfChoosen += numChoice

        return json.dumps(result)

    def _sum_result(self,surveyId):
        sumOfChoosen=0
        survey = Survey.objects.get(id=surveyId)
        options = OptionInSurvey.objects.filter(survey=survey)
        for option in options:
            numChoice = UserChoose.objects.filter(choice=option, survey=survey).count()
            sumOfChoosen += numChoice
        # get number for people who choose this option
        sumOfChoosen

        return sumOfChoosen


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
                "redirect": reverse("event_detail",kwargs={"pk": eventId}),
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