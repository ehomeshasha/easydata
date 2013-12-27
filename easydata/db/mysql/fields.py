'''
Created on Dec 26, 2013

@author: hadoop-user
'''
from django.db import models
from django.db.models.fields import AutoField
from django.db.backends.mysql.creation import DatabaseCreation
from django.core import validators


def get_sign(self, kwargs):
        if 'unsigned' not in kwargs:
            self.unsigned = 'UNSIGNED'
        elif kwargs['unsigned'] == True:
            self.unsigned = 'UNSIGNED'
            del(kwargs['unsigned'])
        else:
            self.unsigned = ''
            del(kwargs['unsigned'])
            
def get_length_str(max_length):
    if max_length:
        lenth_str = '('+str(max_length)+')'
    else:
        lenth_str = ''
    return lenth_str

class C_AutoField(AutoField):
    def __init__(self, *args, **kwargs):
        get_sign(self, kwargs)
        super(C_AutoField, self).__init__(*args, **kwargs)
        self.validators.append(validators.MaxLengthValidator(self.max_length))
    
    def db_type(self, connection):
        return 'int'+get_length_str(self.max_length)+' '+self.unsigned+' AUTO_INCREMENT'
    
    #def get_internal_type(self):
    #    return 'UnsignedAutoField'
#DatabaseCreation.data_types['UnsignedAutoField'] = 'int(%(max_length)s) %(unsigned)s AUTO_INCREMENT'

class C_AutoSmallIntegerField(AutoField):
    def __init__(self, *args, **kwargs):
        get_sign(self, kwargs)
        super(C_AutoSmallIntegerField, self).__init__(*args, **kwargs)
        self.validators.append(validators.MaxLengthValidator(self.max_length))
    
    def db_type(self, connection):
        return 'smallint'+get_length_str(self.max_length)+' '+self.unsigned+' AUTO_INCREMENT'

class C_IntegerField(models.IntegerField):
    def __init__(self, *args, **kwargs):
        get_sign(self, kwargs)
        super(C_IntegerField, self).__init__(*args, **kwargs)
        self.validators.append(validators.MaxLengthValidator(self.max_length))
            
    def db_type(self, connection):
        return 'int'+get_length_str(self.max_length)+' '+self.unsigned

class C_SmallIntegerField(models.SmallIntegerField):
    def __init__(self, *args, **kwargs):
        get_sign(self, kwargs)
        super(C_SmallIntegerField, self).__init__(*args, **kwargs)
        self.validators.append(validators.MaxLengthValidator(self.max_length))
            
    def db_type(self, connection):
        return 'smallint'+get_length_str(self.max_length)+' '+self.unsigned

class C_TinyIntegerField(models.IntegerField):
    def __init__(self, *args, **kwargs):
        get_sign(self, kwargs)
        super(C_TinyIntegerField, self).__init__(*args, **kwargs)
        self.validators.append(validators.MaxLengthValidator(self.max_length))
            
    def db_type(self, connection):
        return 'tinyint'+get_length_str(self.max_length)+' '+self.unsigned


class C_CharField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(C_CharField, self).__init__(*args, **kwargs)
        self.validators.append(validators.MaxLengthValidator(self.max_length))
            
    def db_type(self, connection):
        return 'char'+get_length_str(self.max_length)

class NormalTextField(models.TextField):        
    def db_type(self, connection):
        return 'text'