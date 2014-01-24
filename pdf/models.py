from django.db import models
from django.utils.translation import ugettext_lazy as _
from easydata.db.mysql.fields import C_AutoField, C_IntegerField, C_SmallIntegerField, C_MediumIntegerField, C_TinyIntegerField
from easydata.category.models import category
from easydata.templatetags.custom_tags import hsize

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
    filepn = C_MediumIntegerField(max_length=8, default=0, verbose_name="total page number")
    filepath = models.FilePathField(max_length=300, verbose_name='file path')
    tag = models.CharField(max_length=255)
    cate_id = C_SmallIntegerField(max_length=5, default=0)
    views = C_IntegerField(max_length=10, default=0)
    mark = C_MediumIntegerField(max_length=8, default=0)
    comment = C_MediumIntegerField(max_length=8, default=0)
    date_upload = models.DateTimeField('date uploaded')
    displayorder = C_TinyIntegerField(max_length=1, default=0, unsigned=False)
    isconvert = models.BooleanField(default=0)
    
    def __unicode__(self):
        return self.title
    
    def cate_id_func(self):
        return "%s (id:%d)" % (category.objects.get(pk=self.cate_id).name, self.cate_id)
    cate_id_func.short_description = _('Category')
    
    def filesize_func(self):
        return hsize(self.filesize)
    filesize_func.admin_order_field = 'filesize'
    filesize_func.short_description = _('File size')
    
    def isconvert_func(self):
        return self.isconvert == 1
    isconvert_func.admin_order_field = 'isconvert'
    isconvert_func.boolean = True
    isconvert_func.short_description = _('Is convert')
    
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
    
    def pdf_id_func(self):
        return "%s (id:%d)" % (pdf.objects.get(pk=self.pdf_id).title, self.pdf_id)
    pdf_id_func.short_description = _("target pdf")
    pdf_id_func.admin_order_field = 'pdf_id' 
    
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
    
    def __unicode__(self):
        return self.title
    
    def pdf_id_func(self):
        return "%s (id:%d)" % (pdf.objects.get(pk=self.pdf_id).title, self.pdf_id)
    pdf_id_func.short_description = _("target pdf")
    pdf_id_func.admin_order_field = 'pdf_id' 