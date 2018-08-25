from . import views
from django.urls import path, include

urlpatterns = [

    path('register/', views.RegisterUserView.as_view()),
    path('profile/', views.UserProfileView.as_view(), name="user_profile"),
    path('login/', views.LoginUserView.as_view(), name="user_login"),
    path('reset/', views.ResetUserView.as_view(), name="password_reset"),
    path('logout/', views.LogoutUserView.as_view(), name="user_logout"),

]
