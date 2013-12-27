from django.db import models
from easydata.db.mysql.fields import C_AutoField, C_IntegerField, C_SmallIntegerField, C_CharField, C_AutoSmallIntegerField, C_TinyIntegerField

# Create your models here.
class blog(models.Model):
    bid = C_AutoField(max_length=8, primary_key=True)
    uid = C_IntegerField(max_length=11, default=0)
    username = models.CharField(max_length=30, default="''")
    groupids = models.CharField(max_length=255, default="''")
    title = models.CharField(max_length=100, default="''")
    content = models.TextField()
    cate_id = C_SmallIntegerField(max_length=5, default=0)
    dateline = C_IntegerField(max_length=10, default=0)
    rate_count = C_IntegerField(max_length=10, default=0)
    rate_score = models.CharField(max_length=5, default="''")
    comment_count = C_IntegerField(max_length=10, default=0)
    #tag = C_CharField(max_length=50, default="''")

class comment(models.Model):
    cid = C_AutoField(max_length=10, primary_key=True)
    bid = C_IntegerField(max_length=8, default=0)
    uid = C_IntegerField(max_length=11, default=0)
    username = models.CharField(max_length=30, default="''")
    title = models.CharField(max_length=100, default="''")
    content = models.TextField()
    rate_score = C_TinyIntegerField(max_length=2)
    dateline = C_IntegerField(max_length=10, default=0)
    

class mark(models.Model):
    mid = C_AutoField(max_length=10, primary_key=True)
    bid = C_IntegerField(max_length=8, default=0)
    uid = C_IntegerField(max_length=11, default=0)
    username = models.CharField(max_length=30, default="''")
    title = models.CharField(max_length=100, default="''")
    content = models.CharField(max_length=255, default="''")
    dateline = C_IntegerField(max_length=10, default=0)
    
class relatelinks(models.Model):
    id = C_AutoField(max_length=10, primary_key=True)
    bid = C_IntegerField(max_length=8, default=0)
    url_text = models.CharField(max_length=100, default="''")
    url = models.URLField(default="''")
    


class category(models.Model):
    id = C_AutoSmallIntegerField(max_length=5, primary_key=True)
    fid = C_SmallIntegerField(max_length=5, default=0)
    catename = models.CharField(max_length=30, default="''")
    description = models.CharField(max_length=255, default="''")