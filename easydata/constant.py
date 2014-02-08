import datetime
import time
from django.utils.timezone import utc
from django.utils.translation import ugettext_lazy as _
import re

CONTENT_TYPE = {
    'pdf': 'application/pdf',
    'image': ['image/png','image/jpeg','image/pjpeg','image/gif','image/bmp'],
}

UPLOAD_EXT = {
    'pdf': 'pdf',
    'image': ['png','jpg','jpeg','gif','bmp'],
} 

PDF_UPLOAD_DIR = 'media_files/pdf2html/'


CTYPE_DICT = {
    'pdf': _('PDF'),
    'learning': _('Learning System'),
    'tiku': _('Tiku'),
}
HOME_BREAD = {'text': _('Home'), 'href': '/'}

LANGUAGE_DICT = {
    'en': {'shortname': _("en")},
    'zh-cn': {'shortname': _("zh")},
}