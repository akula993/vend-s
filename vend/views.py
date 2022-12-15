from django.shortcuts import render

from vend.models import Address, Device, Sensor


def home(request):
    address = Address.objects.all()
    devices = Device.objects.all()
    context = {
        'address': address,
        'devices': devices,
    }
    return render(request, 'vend/home.html', context)

def device(request):
    address = Device.objects.all()
    context = {
        'address': address,
    }
    return render(request, 'vend/home.html', context)
