from django.db import models
from easydata.db.mysql.fields import C_SmallIntegerField, C_AutoSmallIntegerField, C_TinyIntegerField

class category(models.Model):
    cid = C_AutoSmallIntegerField(max_length=5, primary_key=True)
    fid = C_SmallIntegerField(max_length=5, default=0)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=255)
    status = C_TinyIntegerField(max_length=1, default=0)
    displayorder = C_SmallIntegerField(max_length=5, default=0)
    ctype = models.CharField(max_length=20)
    
