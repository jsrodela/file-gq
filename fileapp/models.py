from django.db import models

# Create your models here.


class Upload(models.Model):
    code = models.IntegerField()
    temporary = models.BooleanField(default=False)

    index = models.TextField()
    time = models.DateTimeField(auto_now=True)


class FileUpload(models.Model):
    upload_id = models.ForeignKey(Upload,
                                  related_name="upload",
                                  on_delete=models.CASCADE,
                                  db_column="upload_id")
    file = models.FileField(upload_to='')
