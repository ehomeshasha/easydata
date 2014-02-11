from django.db import models
from django.utils.translation import ugettext_lazy as _
from easydata.db.mysql.fields import C_SmallIntegerField, C_AutoField, C_IntegerField
from easydata.category.models import category

class Article(models.Model):
    id = C_AutoField(max_length=8, primary_key=True)
    fid = C_IntegerField(max_length=8, default=0)
    uid = C_IntegerField(max_length=11, default=0)
    username = models.CharField(max_length=30)
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_create = models.DateTimeField('date created')
    date_update = models.DateTimeField('date updated')
    cate_id = C_SmallIntegerField(max_length=5, default=0)
    displayorder = C_SmallIntegerField(max_length=5, default=0)
    
    def __unicode__(self):
        return self.title
    
    def cate_id_func(self):
        return "%s (id:%d)" % (category.objects.get(pk=self.cate_id).name, self.cate_id)
    cate_id_func.short_description = _('Category')
    
    def fid_func(self):
        return "%s (id:%d)" % (ArticleIndex.objects.get(pk=self.fid).title, self.fid)
    cate_id_func.short_description = _('ArticleIndex Title')
    
class ArticleIndex(models.Model):
    id = C_AutoField(max_length=8, primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    uid = C_IntegerField(max_length=11, default=0)
    username = models.CharField(max_length=30)
    cate_id = C_SmallIntegerField(max_length=5, default=0)
    displayorder = C_SmallIntegerField(max_length=5, default=0)
    date_create = models.DateTimeField('date created')
    
    def __unicode__(self):
        return self.title
    
    def cate_id_func(self):
        return "%s (id:%d)" % (category.objects.get(pk=self.cate_id).name, self.cate_id)
    cate_id_func.short_description = _('Category')