from os import listdir
from os.path import isfile, join
from django.contrib import messages
import re
import os

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

def estatic(directory):
    print re.sub(r'^/{0,1}[^/]+/', '/site_media/', directory, count=1)
    return re.sub(r'^/{0,1}[^/]+/', '/site_media/', directory, count=1)