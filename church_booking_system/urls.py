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
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.main.urls')),
    path('accounts/users/', include('apps.user_accounts.urls', namespace='user_accounts')),
    path('accounts/organisations/', include('apps.org_accounts.urls')),
    path('sitemap/', main_views.SitemapView.as_view(), name='sitemap'),
    path('event/', include('apps.events.urls')),
    path('survey/', include('apps.surveys.urls')),
    path('food_preferences/', include('apps.food_preferences.urls', namespace='food_preferences')),

    # TODO: Maybe this should go in user_accounts?
    url(r'^user_confirm/(?P<confirmation_code>.*)/$', UserConfirmView.as_view(), name="user_confirm"),
    # TODO: Maybe these should go in survey?
    path('choose-meal', main_views.ChooseMealView.as_view(), name='choose_meal'),
    path('choose-meal-success', main_views.SuccessView.as_view(), name='general_success'),


] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
