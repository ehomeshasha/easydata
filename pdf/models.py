from django.db import models
from easydata.db.mysql.fields import C_AutoField, C_IntegerField, C_SmallIntegerField, C_MediumIntegerField, C_TinyIntegerField

# Create your models here.
class pdf(models.Model):
    id = C_AutoField(max_length=8, primary_key=True)
    uid = C_IntegerField(max_length=11, default=0)
    username = models.CharField(max_length=30)
    groupids = models.CharField(max_length=255)
    title = models.CharField(max_length=100)
    description = models.TextField()
    filename = models.FileField(max_length=200, upload_to='.')
    filesize = models.CharField(max_length=20)
    filepn = C_MediumIntegerField(max_length=8, default=0)
    filepath = models.FilePathField(max_length=300, verbose_name='file path')
    tag = models.CharField(max_length=255)
    cate_id = C_SmallIntegerField(max_length=5, default=0)
    views = C_IntegerField(max_length=10, default=0)
    mark = C_MediumIntegerField(max_length=8, default=0)
    comment = C_MediumIntegerField(max_length=8, default=0)
    date_upload = models.DateTimeField('date uploaded')
    displayorder = C_TinyIntegerField(max_length=1, default=0, unsigned=False)
    isconvert = C_TinyIntegerField(max_length=1, default=0)
    
    def __unicode__(self):
        return self.title
    
class Mark(models.Model):
    mid = C_AutoField(max_length=10, primary_key=True)
    pdf_id = C_IntegerField(max_length=8, default=0)
    page_num = C_SmallIntegerField(max_length=5, default=0)
    line_num = C_SmallIntegerField(max_length=5, default=0)
    uid = C_IntegerField(max_length=11, default=0)
    username = models.CharField(max_length=30)
    content = models.TextField()
    date_create = models.DateTimeField('create date')
    displayorder = C_TinyIntegerField(max_length=1, default=0, unsigned=False)
    
    def __unicode__(self):
        return str(self.mid)
    
class Comment(models.Model):
    id = C_AutoField(max_length=10, primary_key=True)
    pdf_id = C_IntegerField(max_length=8, default=0)
    uid = C_IntegerField(max_length=11, default=0)
    username = models.CharField(max_length=30)
    title = models.CharField(max_length=100)
    content = models.TextField()
    rate_score = C_TinyIntegerField(max_length=2)
    date_create = models.DateTimeField('create date')
    displayorder = C_TinyIntegerField(max_length=1, default=0, unsigned=False)