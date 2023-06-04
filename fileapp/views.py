from django.shortcuts import render
import random

from . import models


# Create your views here.
def index(request):
    return render(request, 'fileapp/index.html', {
        'hello': 'world',
    })


def send(request):
    if request.method == "POST":
        code = genCode()
        return render(request, 'fileapp/send_result.html', {})

    return render(request, 'fileapp/send.html', {})


def receive(request):
    return render(request, 'fileapp/receive.html', {})


def send_result(request):

    return render(request, 'fileapp/send_result.html', {})


def genCode():
    code = random.randrange(0, 1000000)
    while models.Upload.objects.filter(code=code).exists():
        code = (code + 1) % 1000000
    return code
