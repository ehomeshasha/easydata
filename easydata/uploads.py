from django.utils.translation import ugettext as _
from easydata.constant import CONTENT_TYPE, UPLOAD_EXT
import uuid
from django.http.response import HttpResponse
from easydata.func.function_core import check_login
import os
import json
from easydata.settings import PROJECT_ROOT, MEDIA_URL


def ajax_upload(request):
    user = check_login(request)
    if not user:
        return HttpResponse('{"code":-1,"msg":"%s"}' % _('Please login first'))
    module = request.POST['module']
    upload_type = request.POST['upload_type']
    upload_file = request.FILES['upload_file']
    
    if upload_type == 'image':
        ajax_upload = ImageAjaxUpload(module=module, upload_file=upload_file, username=user.username)
    elif upload_type == 'file':
        ajax_upload = FileAjaxUpload(module=module, upload_file=upload_file, username=user.username)
    
    clean_result = ajax_upload.clean()
    if clean_result:
        return HttpResponse('{"code":-1,"msg":"%s"}' % _(clean_result))
    else:
        ajax_upload.save()
        return HttpResponse(json.dumps(ajax_upload.get_attribute_json()))

class AjaxUpload():
    pass
    
    def __init__(self, **kwargs):
        self.module = kwargs['module']
        self.username = kwargs['username']
        self.upload_file = kwargs['upload_file']
        self.upload_dir = MEDIA_URL+'%s/%s/' % (self.module, self.username)
        self.name = kwargs['upload_file'].name
        self.basename = self.name[:self.name.rfind(".")]
        self.ext = self.name[self.name.rfind(".")+1:]
        self.size = kwargs['upload_file'].size
        self.content_type = kwargs['upload_file'].content_type
        self.target_filename = self.basename+'_'+uuid.uuid4().hex+'.'+self.ext
        self.target_savepath = self.upload_dir + self.target_filename 

    def set_upload_dir(self, upload_dir):
        self.upload_dir = upload_dir
        
    def get_upload_dir(self):
        return self.upload_dir

    def set_target_filename(self, target_filename):
        self.target_filename = target_filename
        
    def get_target_filename(self):
        return self.target_filename
    
    def set_target_savepath(self, target_savepath):
        self.target_savepath = target_savepath
        
    def get_target_savepath(self):
        return self.target_savepath
    
    def clean(self):
        pass
    
    def save(self):
        upload_dir_abs = os.path.join(PROJECT_ROOT, self.upload_dir[1:])
        if not os.path.exists(upload_dir_abs):
            os.makedirs(upload_dir_abs)
        savepath_abs = os.path.join(PROJECT_ROOT, self.target_savepath[1:])
        with open(savepath_abs, 'wb+') as destination:
            for chunk in self.upload_file.chunks():
                destination.write(chunk)
        pass
    
    def get_attribute_json(self):
        json = {'code': 1}
        for attr, value in self.__dict__.iteritems():
            if attr == 'upload_file':
                continue
            json[attr] = value
        return json
    
class ImageAjaxUpload(AjaxUpload):
    
    def clean(self):
        if self.size > 2*1024*1024:
            return _("file too large ( > 2mb )")
        if self.content_type not in CONTENT_TYPE['image']:
            return _("only image is allowed for this upload")
        if self.ext not in UPLOAD_EXT['image']:
            return _("file must be *.png,*.jpg,*.jpeg,*.gif,*.bmp")
        return None
    
class FileAjaxUpload(AjaxUpload):
    def clean(self):
        if self.size > 2*1024*1024:
            return _("file too large ( > 2mb )")
        if self.content_type not in CONTENT_TYPE['file']:
            return _("only compress file or plain/text file is allowed for this upload")
        if self.ext not in UPLOAD_EXT['file']:
            return _("file must be *.zip,*.rar,*.txt,*.gzip,*.gz,*.tar")
        return None
    
    