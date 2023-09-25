from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import random
import json
from . import models


# Create your views here.
def index(request):
    return render(request, 'fileapp/index.html', {})


def send(request):
    if request.method == "POST":
        code = genCode()
        file = request.FILES["file"]

        upload = models.Upload(code=code, )
        upload.save()  # Upload 모델

        fileupload = models.FileUpload(upload_id=upload, file=file)
        fileupload.save()
        return render(request, 'fileapp/send_result.html', {'code': code})

    return render(request, 'fileapp/send.html', {})


def receive(request):
    if request.method == 'POST':
        code = request.POST['code']
    else:
        code = request.GET.get('code', None)

    if code is not None:
        if code == '':
            return render(request, 'fileapp/receive.html', {'error': ''})

        upload = models.Upload.objects.filter(code=int(code)).first()
        if upload is None:
            return render(request, 'fileapp/receive.html', {'error': ''})

        file = models.FileUpload.objects.filter(upload_id=upload).first()
        if file is None:
            return render(request, 'fileapp/receive.html', {'error': ''})

        return redirect(file.file.url)

    return render(request, 'fileapp/receive.html', {})


def send_result(request):
    return render(request, 'fileapp/send_result.html', {})


def genCode():
    code = random.randrange(0, 1000000)
    while models.Upload.objects.filter(code=code).exists():
        code = (code + 1) % 1000000
    return code


@csrf_exempt
def api(request):
    if request.method == "POST":
          code = genCode()
          file = request.FILES["file"]
  
          upload = models.Upload(code=code, )
          upload.save()  # Upload 모델
  
          fileupload = models.FileUpload(upload_id=upload, file=file)
          fileupload.save()
          
          return HttpResponse(json.dumps({
              'status': 'success',
              'code': code
          }))

    return redirect('/')

