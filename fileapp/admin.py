from django.contrib import admin
from . import models

# Register your models here.

class UploadModel(admin.ModelAdmin):
  list_display = ['id', 'code', 'temporary', 'time', 'index', ]
  list_display_links = ['id', 'code']

class FileUploadModel(admin.ModelAdmin):
  list_display = ['id', 'upload_id']
  list_display_links = ['id']
  
admin.site.register(models.Upload, UploadModel)
admin.site.register(models.FileUpload, FileUploadModel)
