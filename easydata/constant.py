'''
Created on Dec 28, 2013

@author: hadoop-user
'''
import datetime
import time
from django.utils.timezone import utc

CONTENT_TYPE = {
    'pdf': 'application/pdf',
    'image': [],
}

PDF_UPLOAD_DIR = '/uploads/pdf/'

NOW = datetime.datetime.utcnow().replace(tzinfo=utc)
TIMESTAMP = int(time.mktime(NOW.timetuple()))