import os
from django.conf import settings
import re
from easydata.func.function_core import elistdir
def mk_upload_dir(directory, **kwarg):
    if kwarg['namelist']:
        for name in kwarg['namelist']:
            directory2 = os.path.join(settings.PROJECT_ROOT, directory +'/'+name)
            if not os.path.exists(directory2):
                os.makedirs(directory2)



def get_upload_dir(directory):
    directory_abs = os.path.join(settings.PROJECT_ROOT, directory)
    if not os.path.exists(directory_abs) or not elistdir(directory_abs+'/pdf', 'file'):
        return directory
    user_dir = os.path.dirname(directory_abs)
    dirname = os.path.basename(directory_abs)
    dirlist = elistdir(user_dir, 'directory')
    if not dirname in dirlist:
        return directory
    else:
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
