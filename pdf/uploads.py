'''
Created on Dec 28, 2013

@author: hadoop-user
'''
from django.conf import settings
from easydata.constant import PDF_UPLOAD_DIR
import uuid
import os
from pdf.func import mk_upload_dir, get_upload_dir




def handle_uploaded_file(store_file, username):
    end_pos = store_file._name.rfind(".")
    filename = store_file._name[:end_pos].replace(" ", "_")
    
    directory = PDF_UPLOAD_DIR+username+'/'+filename
    directory_abs = os.path.join(settings.PROJECT_ROOT, directory)
    if not os.path.exists(directory_abs):
        print "os.makedirs("+directory_abs+")"
        os.makedirs(directory_abs)
    directory = get_upload_dir(directory)
    mk_upload_dir(directory, namelist=['pdf', 'origin', 'new'])
    #print TIMESTAMP
    filepath = directory+'/pdf/'+uuid.uuid4().hex+'.pdf'
    filepath_abs = os.path.join(settings.PROJECT_ROOT, filepath)
    with open(filepath_abs, 'wb+') as destination:
        for chunk in store_file.chunks():
            destination.write(chunk)
    return '/'+filepath
 
 
 

            