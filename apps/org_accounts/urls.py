from . import views
from django.urls import path, include

urlpatterns = [

    path('register/', views.RegisterOrganisationView.as_view()),
    path('profile/', views.OrganisationProfileView.as_view(), name="org_profile"),
    path('', include('django.contrib.auth.urls')),  # URLs for registration and login, logout and password reset

]
