"""church_booking_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.edit import CreateView
from . import views
from django.conf.urls import url
from apps.main.views import SuccessView

urlpatterns = [
    url(r'create/(?P<eventId>[0-9]+)$', views.CreateSurveyView.as_view()),
    url('create/$', views.CreateSurveyView.as_view()),
    path('delete/', views.DeleteSurveyView.as_view()),
    url(r'do/(?P<surveyId>[0-9]+)$', views.DoSurveyView.as_view()),
    path('submit/', views.SubmitSurveyView.as_view()),
    path('close_open/', views.CloseSurveyView.as_view()),
    url(r'result/(?P<surveyId>[0-9]+)$', views.SeeSurveyResultView.as_view()),
    path('success/',views.SuccessView.as_view(),name='survey-success')
    #path('delete/<int:pk>', views.DeleteEventView.as_view()),
    #url(r'^update/(?P<pk>[0-9]+)$',views.UpdateEventView.as_view(), name='event-update'),
    #path('join/', views.JoinEvent.as_view()),
    #url(r'^details/(?P<eventId>[0-9]+)/$', views.EventView.as_view()),
    #path('update/<int:pk>', views.UpdateEventView.as_view(), name='event-update'),

]
