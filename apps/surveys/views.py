from django.http import HttpResponseRedirect
from django.views.generic.edit import DeleteView
from django.shortcuts import render, render_to_response
from django.views.generic.edit import FormView
from django.shortcuts import redirect, reverse
from django.views import generic
from .forms import CreateSurveyForm,CreateOptionForm
from .models import Survey,OptionInSurvey,SurveyParticipation,UserChoose
from apps.food_preferences.models import FoodPreferences
from apps.events.models import Event,InvolvedEvent
import json
import datetime
from apps.core import views as core_views
from django.views.generic import edit
from django.urls import reverse_lazy
from google.cloud import vision
from google.cloud.vision import types
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
    page_title = 'Create Survey!'

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
                "options":OptionInSurvey.objects.filter(survey=survey),
                "preferences":self.generateFoodPreferenceList(survey.event),
                "Npreferences":self.generateNumber(survey.event),
                "view": {
                    'title': self.page_title,
                    'project_name': self.project_name,
                    'profile_page': self.profile_page(),
                    'logout_page': self.logout_page(),
                },
            }

            return render(request, self.template_name, context=context)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


    def post(self, request, *args, **kwargs):
        user = request.user
        if user is None:
            return reverse_lazy('home')
        if user.is_staff:
            operation = request.POST.get("operation", "")
            #print("operation is ",operation)
            surveyId = request.POST.get("survey", "")
            survey = Survey.objects.get(id=surveyId)
            if operation == "add_option":
                files=request.FILES.copy()
                use_img_rcgn= request.POST.get("useImageRecognition","")
                rq = request.POST.copy()
                form = self.option_form_class(rq, files)
                if form.is_valid() and self.usingRecognitionCompletetion(request):
                    print("pass test")
                    option = form.save(commit=False)
                    if Survey.objects.filter(id= surveyId).count()>0:
                        option.survey=survey
                        if use_img_rcgn == "True":
                            option.name = self.performPictureRecognition(request)
                        if option.name=="":
                            form.add_error("name", "picture recognition does not work for this image")

                        else:
                            form=self.option_form_class()
                            option.save()
                        context = {
                            "optionForm":form,
                            "survey": survey,
                            "options": OptionInSurvey.objects.filter(survey=survey),
                            "preferences": self.generateFoodPreferenceList(survey.event),
                            "view": {
                                'title': self.page_title,
                                'project_name': self.project_name,
                                'profile_page': self.profile_page(),
                                'logout_page': self.logout_page(),
                            },

                        }
                        return render(request, self.choice_card_template, context=context)
                #print(form.errors)
                # if user does not enter a name for the option
                form.add_error("name","please enter name for the option or use picture recognition")
                context = {
                    "optionForm": form,
                    "survey": survey,
                    "options": OptionInSurvey.objects.filter(survey=survey),
                    "view": {
                        'title': self.page_title,
                        'project_name': self.project_name,
                        'profile_page': self.profile_page(),
                        'logout_page': self.logout_page(),
                    },

                }
                return render(request, self.choice_card_template, context=context)

            elif operation == "create_survey":
                if(OptionInSurvey.objects.filter(survey=survey).count()<1):
                    context = {
                        "surveyForm": self.survey_form_class(),
                        "optionForm": self.option_form_class(),
                        "survey": survey,
                        "error":"More options are needed to form a survey",
                        "options": OptionInSurvey.objects.filter(survey=survey),
                        "preferences": self.generateFoodPreferenceList(survey.event),
                        "view": {
                            'title': self.page_title,
                            'project_name': self.project_name,
                            'profile_page': self.profile_page(),
                            'logout_page': self.logout_page(),
                        },

                    }
                    return render(request, self.template_name, context=context)
                form = self.survey_form_class(request.POST)
                #print("creating survey")
                if form.is_valid():
                    survey.title=request.POST.get("title", "")
                    survey.isFinalized=True
                    survey.save()
                    return render(request, self.success_template, context=self.generateSuccessContext(survey))
                context = {
                    "surveyForm":form,
                    "optionForm": self.option_form_class(),
                    "survey": survey,
                    "options": OptionInSurvey.objects.filter(survey=survey),
                    "preferences": self.generateFoodPreferenceList(survey.event),
                    "view": {
                        'title': self.page_title,
                        'project_name': self.project_name,
                        'profile_page': self.profile_page(),
                        'logout_page': self.logout_page(),
                    },

                }
                return render(request, self.template_name, context=context)

    def usingRecognitionCompletetion(self,request):
        if request.POST.get("name","") =="":
            if request.POST.get("useImageRecognition","")=="True" and len(request.FILES) >0:
                return True
            else:
                return False
        else:
            return True


    def performPictureRecognition(self,request):
        result=""
        try:
            pass
            result=self.pictureRecognition(request.FILES['imageFile'].read())
        except:
            result="as shown at the picture"
            print("error")
        return result

    def generateFoodPreferenceList(self,event):
        participants = [involment.participant for involment in InvolvedEvent.objects.filter(event=event)]
        foodPreferences = [FoodPreferences.objects.get(user=participant) for participant in participants
                           if FoodPreferences.objects.filter(user=participant).count()>0]
        #print("search preference "+str(len(foodPreferences)))
        result={
        "vegetarian": InvolvedEvent.objects.filter(event=event).
            select_related('participant__foodpreferences').filter(participant__foodpreferences__vegetarian=True).count(),
        "vegan": InvolvedEvent.objects.filter(event=event).
            select_related('participant__foodpreferences').filter(participant__foodpreferences__vegan=True).count(),
        "nut allergy": InvolvedEvent.objects.filter(event=event).
            select_related('participant__foodpreferences').filter(participant__foodpreferences__nut_allergy=True).count(),
        "egg allergy": InvolvedEvent.objects.filter(event=event).
            select_related('participant__foodpreferences').filter(participant__foodpreferences__egg_allergy=True).count(),
        "dairy allergy": InvolvedEvent.objects.filter(event=event).
            select_related('participant__foodpreferences').filter(participant__foodpreferences__dairy_allergy =True).count(),
        "soy allergy": InvolvedEvent.objects.filter(event=event).
            select_related('participant__foodpreferences').filter(participant__foodpreferences__soy_allergy=True).count(),
        "shellfish allergy": InvolvedEvent.objects.filter(event=event).
            select_related('participant__foodpreferences').filter(participant__foodpreferences__shellfish_allergy=True).count(),
        "fish allergy": InvolvedEvent.objects.filter(event=event).
            select_related('participant__foodpreferences').filter(participant__foodpreferences__fish_allergy=True).count(),
        }
        #print(result)
        return result

    def generateNumber(self,event):
        participants = [involment.participant for involment in InvolvedEvent.objects.filter(event=event)]
        foodPreferences = [FoodPreferences.objects.get(user=participant) for participant in participants
                           if FoodPreferences.objects.filter(user=participant).count()>0]
        print("search preference "+str(len(foodPreferences)))
        result={
        "vegetarian": InvolvedEvent.objects.filter(event=event).
            select_related('participant__foodpreferences').filter(participant__foodpreferences__vegetarian=True).count(),
        "vegan": InvolvedEvent.objects.filter(event=event).
            select_related('participant__foodpreferences').filter(participant__foodpreferences__vegan=True).count(),
        "nut allergy": InvolvedEvent.objects.filter(event=event).
            select_related('participant__foodpreferences').filter(participant__foodpreferences__nut_allergy=True).count(),
        "egg allergy": InvolvedEvent.objects.filter(event=event).
            select_related('participant__foodpreferences').filter(participant__foodpreferences__egg_allergy=True).count(),
        "dairy allergy": InvolvedEvent.objects.filter(event=event).
            select_related('participant__foodpreferences').filter(participant__foodpreferences__dairy_allergy =True).count(),
        "soy allergy": InvolvedEvent.objects.filter(event=event).
            select_related('participant__foodpreferences').filter(participant__foodpreferences__soy_allergy=True).count(),
        "shellfish allergy": InvolvedEvent.objects.filter(event=event).
            select_related('participant__foodpreferences').filter(participant__foodpreferences__shellfish_allergy=True).count(),
        "fish allergy": InvolvedEvent.objects.filter(event=event).
            select_related('participant__foodpreferences').filter(participant__foodpreferences__fish_allergy=True).count(),
        }
        return sum(result.values())


    def pictureRecognition(self,pic):
        if pic is not None:
            client = vision.ImageAnnotatorClient()
            image = types.Image(content=pic)
            # Performs label detection on the image file
            response = client.label_detection(image=image)
            labels = response.label_annotations
            print(self.findValidLabel(labels))
            return self.findValidLabel(labels)
        return ""


    def findValidLabel(self,labels):
        usless_label= ["food", "cuisine", "dish"]
        for label in labels:
            if label.description in usless_label:
                continue
            if label.score >0.85:
                return label.description
        return ""

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

class DeleteOptionInSurvey(DeleteView):
    model = OptionInSurvey

    def get_success_url(self, **kwargs):
        print(self.object.survey.event.id)
        return reverse_lazy('add_option_for_survey',args=(self.object.survey.event.id,self.object.survey.id,))


class SubmitSurveyView(generic.TemplateView, core_views.BaseView):

    template_name = "survey_response.html"
    page_title = "Submit"
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
                    return render(request, self.template_name, context=context)

            else:
                #the user is not in this event
                context["isSuccess"]=False
                context["message"] = "you have not join this event yet"
                context[ "view"]= {
                            'title': self.page_title,
                            'project_name': self.project_name,
                            'profile_page': self.profile_page(),
                            'logout_page': self.logout_page(),
                        }


                return render(request, self.template_name, context=context)


        else:
            context["message"] = "you should login before submit a anything"
            if optionId == "":
                context["message"] = "you should choose a option before submit"
            return render(request, self.template_name, context=context)

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


class DoSurveyView(generic.View, core_views.BaseView):
    template_name = 'do_survey.html'
    success_template = 'survey_response.html'
    page_title = "Fill out the survey"
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
                "view": {
                    'title': self.page_title,
                    'project_name': self.project_name,
                    'profile_page': self.profile_page(),
                    'logout_page': self.logout_page(),
                },
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

class SeeSurveyResultView(generic.View, core_views.BaseView):

    template_name = 'view_survey_result.html'
    page_title = "Results"

    def get(self, request,surveyId):
        print(surveyId)
        summary=self._construct_result(surveyId)
        survey = Survey.objects.get(id=surveyId)
        options = OptionInSurvey.objects.filter(survey=survey)
        sumOfChoosen = 0
        prevent_zero =lambda x:1 if x == 0 else x
        context={
            "survey":survey,
            "options":options,
            "summary":summary,
            "chart_data":self._construct_json_result(surveyId,sumOfChoosen),
            "sumOfChoosen":self._sum_result(surveyId),
            "participation_rate": SurveyParticipation.objects.filter(survey=survey).filter().count() * 100 /
                                  prevent_zero(InvolvedEvent.objects.filter(event=survey.event).count()),
            "survey_participant":SurveyParticipation.objects.filter(survey=survey).filter().count() ,
            "event_participant":InvolvedEvent.objects.filter(event=survey.event).count(),
            "view": {
                'title': self.page_title,
                'project_name': self.project_name(),
                'profile_page': self.profile_page(),
                'logout_page': self.logout_page(),
            },
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


class ProcessSurvey(generic.View, core_views.BaseView):
    template_name = 'event_offer.html'
    success_template = 'survey_response.html'
    model = Survey
    page_title = "Survey Response"

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

                            context = {
                                'error': error,
                                "isSuccess": False,
                                "event": Event.objects.get(id=int(eventId)),
                                "view": {
                                    'title': self.page_title,
                                    'project_name': self.project_name,
                                    'profile_page': self.profile_page(),
                                    'logout_page': self.logout_page(),
                                },
                            }
                            # not a valid option
                            error = "please add some choice to a survey"
                            return render(request, self.template_name, context)
            return render(request, self.success_template, self._define_success_context(error,eventId))
        except:
            error = "invalid input"
            context = {
                'error': error,
                "isSuccess": False,
                "event": Event.objects.get(id=int(eventId)),
                "view": {
                    'title': self.page_title,
                    'project_name': self.project_name,
                    'profile_page': self.profile_page(),
                    'logout_page': self.logout_page(),
                },
            }
            return render(request, self.template_name, context)

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





class SuccessView(generic.TemplateView, core_views.BaseView):
    template_name = 'survey_response.html'
    page_title = "Success"
