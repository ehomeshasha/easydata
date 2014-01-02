import os
import re
from django.conf import settings
from os import listdir
from os.path import isfile, join
def get_upload_dir(directory):
    directory_abs = os.path.join(settings.PROJECT_ROOT, directory)
    user_dir = os.path.dirname(directory_abs)
    dirname = os.path.basename(directory_abs)
    dirlist = elistdir(user_dir, 'directory')
    print dirlist
    print dirname
    if not dirname in dirlist:
        return directory
    else:
        print directory
        pattern = re.compile(dirname+'_(\d+)')
        max_num = 0
        for subdir in dirlist:
            match = re.search(pattern, subdir)
            if match:
                n = int(match.group(1)) + 1
                if n > max_num:
                    max_num = n
            else:
                continue
        return directory+'_'+str(max_num)
        
    #pattern = re.compile(directory+'_(\d+)')
    #match = re.search(pattern, directory)
    #if os.path.exists(directory):
    #    pass
def elistdir(directory, find_type='all'):
    if find_type == 'all':
        return [ f for f in listdir(directory)]
    elif find_type =='file':
        return [ f for f in listdir(directory) if isfile(join(directory,f)) ]
    elif find_type == 'directory':
        return [ f for f in listdir(directory) if not isfile(join(directory,f)) ]
    return []       
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "easydata.settings")
directory = "pdf/static/pdf/pdf2html/zzy2/Hadoop_in_Action"

print get_upload_dir(directory)