from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import random
import json
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse
from urllib import parse

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

        if code is not None:
            if code == '':
                return render(request, 'fileapp/receive.html', {'error': ''})
    
            upload = models.Upload.objects.filter(code=int(code)).first()
            if upload is None:
                return render(request, 'fileapp/receive.html', {'error': ''})

            # file = models.FileUpload.objects.filter(upload_id=upload).first()
            # if file is None:
            #     return render(request, 'fileapp/receive.html', {'error': ''})
    
            response = get_file_response(upload)
            if response is None:
                return render(request, 'fileapp/receive.html', {'error': ''})

            return response
            
            # return redirect(file.file.url)
    else:
        # code = request.GET.get('code', None)
        return render(request, 'fileapp/receive.html', {})


def get_file_response(upload):
  file_upload = models.FileUpload.objects.filter(upload_id=upload).first()
  if file_upload is None:
      return None
  file_path = file_upload.file.path
  file_name = file_upload.file.name
  fs = FileSystemStorage(file_path)

  response = FileResponse(fs.open(file_path, 'rb'), content_type='multipart/form-data;')
  response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'%s' % parse.quote(file_name)
  return response


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

