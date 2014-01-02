'''
Created on Dec 28, 2013

@author: hadoop-user
'''
from django.conf import settings
from easydata.constant import TIMESTAMP, PDF_UPLOAD_DIR, TEXT_UPLOAD_DIR, IMAGE_UPLOAD_DIR
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
    image_dir = os.path.join(settings.PROJECT_ROOT, IMAGE_UPLOAD_DIR[1:])
    filepath_convert = TEXT_UPLOAD_DIR+filename+'_T'+str(TIMESTAMP)+'_'+uuid.uuid4().hex
    filepath_convert_text = filepath_convert + '.txt'
    filepath_convert_html = filepath_convert + '.html'
    filepath_convert_xml = filepath_convert + '.xml'
    filepath_convert_tag = filepath_convert + '.tag'
    filepath_convert_text_abs = os.path.join(settings.PROJECT_ROOT, filepath_convert_text[1:])
    filepath_convert_html_abs = os.path.join(settings.PROJECT_ROOT, filepath_convert_html[1:])
    filepath_convert_xml_abs = os.path.join(settings.PROJECT_ROOT, filepath_convert_xml[1:])
    filepath_convert_tag_abs = os.path.join(settings.PROJECT_ROOT, filepath_convert_tag[1:])
    print "pdf2txt.py -o "+filepath_convert_text_abs+" -t text -I "+image_dir+" "+filepath_save
    os.system("pdf2txt.py -o "+filepath_convert_text_abs+" -t text -I "+image_dir+" "+filepath_save)
    os.system("pdf2txt.py -o "+filepath_convert_html_abs+" -t html -I "+image_dir+" "+filepath_save)
    os.system("pdf2txt.py -o "+filepath_convert_xml_abs+" -t xml -I "+image_dir+" "+filepath_save)
    os.system("pdf2txt.py -o "+filepath_convert_tag_abs+" -t tag -I "+image_dir+" "+filepath_save)
    
    
    
    return filepath
        