'''
Created on Dec 28, 2013

@author: hadoop-user
'''
from django.conf import settings
from django import forms as django_forms
from easydata.constant import CONTENT_TYPE, TIMESTAMP, PDF_UPLOAD_DIR
from django.utils.translation import ugettext_lazy as _
import uuid
import os


def handle_uploaded_file(store_file):
    end_pos = store_file._name.rfind(".")
    filename = store_file._name[:end_pos].replace(" ", "_")
    #print TIMESTAMP
    filepath = PDF_UPLOAD_DIR+filename+'_T'+str(TIMESTAMP)+'_'+uuid.uuid4().hex+'.pdf'
    filepath_save = os.path.join(settings.PROJECT_ROOT, filepath[1:])
    with open(filepath_save, 'wb+') as destination:
        for chunk in store_file.chunks():
            destination.write(chunk)
    
    return filepath
        