'''
Created on Dec 26, 2013

@author: hadoop-user
'''
from django.db import models

class NormalTextField(models.TextField):        
    def db_type(self, connection):
        return 'text'