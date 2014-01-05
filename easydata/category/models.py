from django.db import models
from easydata.db.mysql.fields import C_AutoField, C_IntegerField, C_SmallIntegerField, C_CharField, C_AutoSmallIntegerField, C_TinyIntegerField

class category(models.Model):
    id = C_AutoSmallIntegerField(max_length=5, primary_key=True)
    fid = C_SmallIntegerField(max_length=5, default=0)
    catename = models.CharField(max_length=30)
    description = models.CharField(max_length=255)
    displayorder = C_SmallIntegerField(max_length=5, default=0)