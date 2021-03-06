from django.conf import settings
from easydata.constant import PDF_UPLOAD_DIR
import uuid
import os
from pdf.func import mk_upload_dir, get_upload_dir
import re



def handle_uploaded_file(store_file, username):
    end_pos = store_file._name.rfind(".")
    
    filename = re.sub(r'\W+', '', store_file._name[:end_pos])
    
    directory = PDF_UPLOAD_DIR+username+'/'+filename
    directory = get_upload_dir(directory)
    mk_upload_dir(directory, namelist=['pdf', 'origin', 'new'])

    filepath = directory+'/pdf/'+uuid.uuid4().hex+'.pdf'
    filepath_abs = os.path.join(settings.PROJECT_ROOT, filepath)
    with open(filepath_abs, 'wb+') as destination:
        for chunk in store_file.chunks():
            destination.write(chunk)
    return '/'+filepath
 
 
 

            