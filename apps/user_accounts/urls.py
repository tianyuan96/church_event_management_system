from . import views
from django.urls import path, include
from django.conf.urls import url

app_name = 'user_accounts'

urlpatterns = [

    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('profile/', views.UserProfileView.as_view(), name="profile"),
    path('login/', views.LoginUserView.as_view(), name="login"),
    path('reset/', views.ResetUserView.as_view(), name="password_reset"),
    path('logout/', views.LogoutUserView.as_view(), name="logout"),

    path('update/<int:pk>', views.UpdateUserView.as_view(), name="update_user"),

    path('successfully_registered/', views.NeedActivateView.as_view(), name="successfully_registered"),
    url(r'^user_confirm/(?P<confirmation_code>.*)/$', views.UserConfirmView.as_view(), name="user_confirm"),
    path('successfully_confirmed/', views.HasActivatedView.as_view(), name="successfully_confirmed"),

]
