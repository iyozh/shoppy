from django.conf.urls import url
from . import views
from .apps import OrdersConfig

app_name = OrdersConfig.label

urlpatterns = [
    url(r'^create/$', views.order_create, name='order_create'),
]