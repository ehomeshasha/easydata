from django.utils.translation import ugettext_lazy as _

CONTENT_TYPE = {
    'pdf': 'application/pdf',
    'image': ['image/png','image/jpeg','image/pjpeg','image/gif','image/bmp'],
    'file': ['application/x-compressed',
             'application/x-zip-compressed',
             'application/zip',
             'multipart/x-zip',
             'application/x-rar-compressed',
             'application/octet-stream',
             'text/plain',
             'multipart/x-gzip',
             'application/x-gzip',
             'application/x-compressed',
             'application/x-tar'
             ]
    
}

UPLOAD_EXT = {
    'pdf': 'pdf',
    'image': ['png','jpg','jpeg','gif','bmp'],
    'file': ['zip','rar','txt','gzip','gz','tar'],
} 

PDF_UPLOAD_DIR = 'media_files/pdf2html/'


CTYPE_DICT = {
    'pdf': _('PDF'),
    'learning': _('Learning System'),
    'tiku': _('Tiku'),
}
HOME_BREAD = {'text': _('Home'), 'href': '/'}

LANGUAGE_DICT = {
    'en': {'shortname': _("en"), 'tinymce': 'en'},
    'zh-cn': {'shortname': _("zh"), 'tinymce': 'zh_CN'},
}

PERPAGE = 20


PERMISSION_ERROR = {
    'level': 'ERROR',
    'title': _('Permission Error'),
    'body':_('You\'re not allowed to handle this request'),
}
