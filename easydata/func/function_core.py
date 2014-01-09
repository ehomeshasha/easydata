from os import listdir
from os.path import isfile, join
from django.contrib import messages
import time
from django.utils.timezone import now

def check_login(request):
    if request.user.is_authenticated():
            User = request.user
    else:
        messages.add_message(
            request,
            messages.WARNING,
            'Please login first',
        )
        return False
    return User

def elistdir(directory, find_type='all'):
    if find_type == 'all':
        return [ f for f in listdir(directory)]
    elif find_type =='file':
        return [ f for f in listdir(directory) if isfile(join(directory,f)) ]
    elif find_type == 'directory':
        return [ f for f in listdir(directory) if not isfile(join(directory,f)) ]
    return []

#h means human-readable
def get_hsize(size):
    num = int(size)
    for x in ['bytes','KB','MB','GB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')

def get_timestamp():
    return int(time.mktime(now().timetuple()))


