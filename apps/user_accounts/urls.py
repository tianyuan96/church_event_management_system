from . import views
from django.urls import path, include
from django.conf.urls import url

urlpatterns = [

    path('register/', views.RegisterUserView.as_view()),
    path('profile/', views.UserProfileView.as_view(), name="user_profile"),
    path('login/', views.LoginUserView.as_view(), name="user_login"),
    path('reset/', views.ResetUserView.as_view(), name="password_reset"),
    path('logout/', views.LogoutUserView.as_view(), name="user_logout"),
    path('successfully_registered/', views.NeedActivateView.as_view(), name="successfully_registered"),
    path('back_homepage/', views.BackHomepageView.as_view(), name="back_home_page"),
    url(r'^user_confirm/(?P<confirmation_code>.*)/$', views.UserConfirmView.as_view(), name="user_confirm"),
    path('successfully_confirmed/', views.HasActivatedView.as_view(), name="successfully_confirmed"),

]
