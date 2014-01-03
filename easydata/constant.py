import datetime
import time
from django.utils.timezone import utc

CONTENT_TYPE = {
    'pdf': 'application/pdf',
    'image': [],
}

PDF_UPLOAD_DIR = 'media_files/pdf2html/'


NOW = datetime.datetime.utcnow().replace(tzinfo=utc)
TIMESTAMP = int(time.mktime(NOW.timetuple()))