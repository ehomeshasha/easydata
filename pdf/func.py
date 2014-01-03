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
    if not os.path.exists(directory_abs):
        os.makedirs(directory_abs)
        return directory
    
