from django.db import models
from easydata.db.mysql.fields import C_SmallIntegerField, C_TinyIntegerField,\
    C_MediumIntegerField, C_AutoField, C_IntegerField

class Code(models.Model):
    id = C_AutoField(max_length=8, primary_key=True)
    code = models.TextField()
    title = models.CharField(max_length=30)
    cate_id = C_SmallIntegerField(max_length=5, default=0)
    description = models.CharField(max_length=255)
    uid = C_IntegerField(max_length=11, default=0)
    username = models.CharField(max_length=30)
    brush = models.CharField(max_length=20)
    gutter =  C_TinyIntegerField(max_length=1, default=0)
    first_line = C_SmallIntegerField(max_length=5, default=1)
    collapse = C_TinyIntegerField(max_length=1, default=0)
    highlight = models.CharField(max_length=255)
    url_clickable = C_TinyIntegerField(max_length=1, default=0)
    displayorder = C_SmallIntegerField(max_length=5, default=0)
    mark = C_MediumIntegerField(max_length=8, default=0)
    date_create = models.DateTimeField('date created')
    date_update = models.DateTimeField('date updated')
    
    def __unicode__(self):
        return str(self.title)
    
    
class Mark(models.Model):
    mid = C_AutoField(max_length=10, primary_key=True)
    code_id = C_IntegerField(max_length=8, default=0)
    line_num = C_SmallIntegerField(max_length=5, default=0)
    uid = C_IntegerField(max_length=11, default=0)
    username = models.CharField(max_length=30)
    content = models.TextField()
    date_create = models.DateTimeField('create date')
    displayorder = C_TinyIntegerField(max_length=1, default=0, unsigned=False)
    
    def __unicode__(self):
        return str(self.mid)
    
    
