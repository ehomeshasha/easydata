'''
Created on Dec 28, 2013

@author: hadoop-user
'''
from django.conf import settings
from easydata.constant import PDF_UPLOAD_DIR
import uuid
import os


def handle_uploaded_file(store_file, username):
    end_pos = store_file._name.rfind(".")
    filename = store_file._name[:end_pos].replace(" ", "_")
    #print TIMESTAMP
    filepath = PDF_UPLOAD_DIR+username+'/'+filename+'/'+uuid.uuid4().hex+'.pdf'
    filepath_save = os.path.join(settings.PROJECT_ROOT, filepath[1:])
    with open(filepath_save, 'wb+') as destination:
        for chunk in store_file.chunks():
            destination.write(chunk)
    return filepath
        