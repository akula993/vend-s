from django.shortcuts import render

from vend.models import Addres, Device


def home(request):
    address = Addres.objects.all()
    url = Device.get_absolute_url()
    print(address)
    context = {
        'address': address,
        'url': url,
    }
    return render(request, 'vend/home.html', context)

def device(request):
    address = Device.objects.all()
    context = {
        'address': address,
    }
    return render(request, 'vend/home.html', context)