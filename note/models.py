from django.db import models
from easydata.db.mysql.fields import C_SmallIntegerField, C_AutoField, C_IntegerField

class Note(models.Model):
    id = C_AutoField(max_length=8, primary_key=True)
    uid = C_IntegerField(max_length=11, default=0)
    username = models.CharField(max_length=30)
    content = models.TextField()
    date_create = models.DateTimeField('date created')
    date_update = models.DateTimeField('date updated')
    displayorder = C_SmallIntegerField(max_length=5, default=0)
    
