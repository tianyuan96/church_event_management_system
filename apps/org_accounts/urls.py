from . import views
from django.urls import path, include

urlpatterns = [

    path('register/', views.RegisterOrganisationView.as_view(), name='org_register'),
    path('profile/', views.OrganisationProfileView.as_view(), name="org_profile"),
    path('login/', views.LoginOrganisationView.as_view(), name="org_login"),
    path('logout/', views.LogoutOrganisationView.as_view(), name="org_logout"),

]
