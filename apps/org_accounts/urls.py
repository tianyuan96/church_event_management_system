from . import views
from django.urls import path, include

app_name = 'org_accounts'

urlpatterns = [

    path('register/', views.RegisterOrganisationView.as_view(), name='register'),
    path('profile/', views.OrganisationProfileView.as_view(), name="profile"),
    path('login/', views.LoginOrganisationView.as_view(), name="login"),
    path('logout/', views.LogoutOrganisationView.as_view(), name="logout"),
    path('update/<int:pk>', views.UpdateUserView.as_view(), name="update"),

]
