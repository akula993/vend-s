from django.http import HttpResponseNotFound
from django.shortcuts import render


def badRequest(request, exception):
    return render(request, 'error/400.html', status=404)
def permissionDenied(request, exception):
    return render(request, 'error/403.html', status=404)
def pageNotFound(request, exception):
    return render(request, 'error/404.html', status=404)
def serverError(request, exception):
    return render(request, 'error/500.html', status=404)