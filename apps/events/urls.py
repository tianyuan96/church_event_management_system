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

urlpatterns = [
    path('create/', views.CreateEventView.as_view(), name='event_create'),
    path('details/<int:pk>', views.EventDetailsView.as_view(), name='event_details'),

    path('delete/<int:pk>', views.DeleteEventView.as_view()),
    url(r'^update/(?P<pk>[0-9]+)$',views.UpdateEventView.as_view(), name='event_update'),
    path('success', views.CreateSuccessView.as_view(), name='event_success'),
    path('join/', views.JoinEvent.as_view()),
    url(r'^discussion/(?P<eventID>[0-9]+)/$', views.PostCreationView.as_view(), name='event_forums'),
    url(r'^updatepost/(?P<pk>[0-9]+)$',views.UpdatePostView.as_view(), name='post_update'),
    path('deletepost/<int:pk>', views.DeletePostView.as_view()),

]
