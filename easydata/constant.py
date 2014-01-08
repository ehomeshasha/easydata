import datetime
import time
from django.utils.timezone import utc
from django.utils.translation import ugettext as _

CONTENT_TYPE = {
    'pdf': 'application/pdf',
    'image': [],
}

PDF_UPLOAD_DIR = 'media_files/pdf2html/'

CTYPE_DICT = {
    'pdf': _('PDF'),
    'learning': _('Learning System'),
    'tiku': _('Tiku'),
}
