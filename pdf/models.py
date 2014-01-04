from django.db import models
from easydata.db.mysql.fields import C_AutoField, C_IntegerField, C_SmallIntegerField,C_MediumIntegerField, C_CharField, C_AutoSmallIntegerField, C_TinyIntegerField

# Create your models here.
class pdf(models.Model):
    id = C_AutoField(max_length=8, primary_key=True)
    uid = C_IntegerField(max_length=11, default=0)
    username = models.CharField(max_length=30)
    groupids = models.CharField(max_length=255)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    filename = models.FileField(max_length=200, upload_to='.')
    filesize = models.CharField(max_length=20)
    filepath = models.FilePathField(max_length=300, verbose_name='file path')
    tag = models.CharField(max_length=255)
    cate_id = C_SmallIntegerField(max_length=5, default=0)
    views = C_IntegerField(max_length=10, default=0)
    mark = C_MediumIntegerField(max_length=8, default=0)
    comment = C_MediumIntegerField(max_length=8, default=0)
    date_upload = models.DateTimeField('date uploaded')
    displayorder = C_TinyIntegerField(max_length=1, default=0)
    isconvert = C_TinyIntegerField(max_length=1, default=0)
    

