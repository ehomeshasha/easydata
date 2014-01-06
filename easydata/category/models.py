from django.db import models
from easydata.db.mysql.fields import C_AutoField, C_IntegerField, C_SmallIntegerField, C_CharField, C_AutoSmallIntegerField, C_TinyIntegerField

class category(models.Model):
    cid = C_AutoSmallIntegerField(max_length=5, primary_key=True)
    fid = C_SmallIntegerField(max_length=5, default=0)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=255)
    status = C_TinyIntegerField(max_length=1, default=0)
    displayorder = C_SmallIntegerField(max_length=5, default=0)
    ctype = models.CharField(max_length=20)
    
    
'''
CREATE TABLE easydata_category(
   id int(5) UNSIGNED NOT NULL AUTO_INCREMENT primary key,
   fid int(5) UNSIGNED NOT NULL DEFAULT '0',
   catename varchar(30) NOT NULL DEFAULT '',
   description varchar(255) NOT NULL DEFAULT '',
   displayorder smallint(5) NOT NULL DEFAULT '0'
);
'''