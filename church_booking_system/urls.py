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
from apps.main import views as main_views
from apps.user_accounts.views import UserConfirmView
from django.conf.urls import url


urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', main_views.HomeView.as_view(), name='home'),
    path('accounts/users/', include('apps.user_accounts.urls')),
    path('accounts/organisations/', include('apps.org_accounts.urls')),
    path('choose-meal', main_views.ChooseMealView.as_view(), name='choose_meal'),
    url(r'^user_confirm/(?P<confirmation_code>.*)/$', UserConfirmView.as_view(), name="user_confirm"),

]
