from . import views
from django.urls import path, include

urlpatterns = [

    path('register/', views.RegisterAccountView.as_view()),
    path('profile/', views.ProfileView.as_view(), name="profile"),

]
