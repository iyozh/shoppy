from django.urls import path
from . import views
from .apps import AuthAppConfig

app_name = AuthAppConfig.label

urlpatterns = [
 path('sign-in/', views.SignIn.as_view(), name="sign-in"),
 path('sign-up/', views.signup, name='sign-up'),
 path('logout/', views.CustomLogoutView.as_view(), name='logout'),
 path('confirm/', views.confirm_account, name='confirm-page'),
]