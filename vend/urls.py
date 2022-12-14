from django.urls import path

from vend.views import home, device

urlpatterns = [
    path('', home, name='home'),
    path('<slug:slug_name>/', device, name='address'),
    path('post/<int:post_id>/', device, name='device'),
]
