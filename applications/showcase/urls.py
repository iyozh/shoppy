from django.urls import path
from . import views
from .apps import ShowcaseConfig

app_name = ShowcaseConfig.label

urlpatterns = [
 path('', views.home, name='home')
]