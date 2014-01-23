from django.db import models
from django.utils.translation import ugettext_lazy as _
from easydata.db.mysql.fields import C_SmallIntegerField, C_TinyIntegerField,\
    C_MediumIntegerField, C_AutoField, C_IntegerField
from easydata.category.models import category

class Code(models.Model):
    id = C_AutoField(max_length=8, primary_key=True)
    code = models.TextField()
    title = models.CharField(max_length=100)
    cate_id = C_SmallIntegerField(max_length=5, default=0, verbose_name=_("Category"))
    description = models.CharField(max_length=255)
    uid = C_IntegerField(max_length=11, default=0)
    username = models.CharField(max_length=30)
    brush = models.CharField(max_length=20, verbose_name=_("Language"))
    gutter =  C_TinyIntegerField(max_length=1, default=0)
    first_line = C_SmallIntegerField(max_length=5, default=1)
    collapse = C_TinyIntegerField(max_length=1, default=0)
    highlight = models.CharField(max_length=255)
    url_clickable = C_TinyIntegerField(max_length=1, default=0)
    max_height = models.CharField(max_length=20)
    displayorder = C_SmallIntegerField(max_length=5, default=0)
    mark = C_MediumIntegerField(max_length=8, default=0)
    date_create = models.DateTimeField('date created')
    date_update = models.DateTimeField('date updated')
    
    def cate_id_func(self):
        return "%s (id:%d)" % (category.objects.get(pk=self.cate_id).name, self.cate_id)
    cate_id_func.short_description = _('Category')
    
    def brush_func(self):
        return self.brush.title()
    brush_func.short_description = _('Language')
    brush_func.admin_order_field = 'brush'
    
    def __unicode__(self):
        return self.title
    
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
    
    def code_id_func(self):
        return "%s (id:%d)" % (Code.objects.get(pk=self.code_id).title, self.code_id)
    code_id_func.short_description = _("target code")
    code_id_func.admin_order_field = 'code_id' 
    
