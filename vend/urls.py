from django.urls import path

from vend.views import *

urlpatterns = [
    path('', home, name='home'),
    path('<str:slug>/', address, name='address'),
    path('device/<int:device_id>/', device, name='device'),
]



