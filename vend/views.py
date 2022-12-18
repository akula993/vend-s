from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from vend.models import Address, Device, Sensor, Sensor_win


def home(request):
    address = Address.objects.all()
    context = {
        'address': address,

    }
    return render(request, 'vend/home.html', context)


def address(request, slug):
    address = Address.objects.filter(slug=slug)
    device = Device.objects.all()
    context = {
        'address': address,
        'device':device
    }
    return render(request, 'vend/address_detail.html', context)

def device(request, device_id):
    device = Device.objects.filter(pk=device_id)
    sensor = Sensor.objects.all()
    sensor_win = Sensor_win.objects.all()
    context = {
        'device': device,
        'sensor': sensor,
        'sensor_win': sensor_win,
    }
    return render(request, 'vend/device_detail.html', context)