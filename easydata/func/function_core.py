from os import listdir
from os.path import isfile, join
from django.contrib import messages
import time
from django.utils.timezone import now
from easydata.settings import cursor
from easydata.func.function_db import dictfetchall

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



'''
function get_categorytree($fid = 0, $level = 0 ,$ctype = '') {
    $tree = array();
    $level++;
    
    if($ctype == '') {
        $query = DB::query("SELECT ctype FROM ".DB::table('aut_category')." WHERE status>0 GROUP BY ctype");
        while($value = DB::fetch($query)) {
            $tree[$value['ctype']] = get_categorytree(0, 0, $value['ctype']);
        }
        return $tree;
    }
    $query = DB::query("SELECT cid,fid,name,description FROM ".DB::table('aut_category')." WHERE status>0 AND ctype='$ctype' AND fid=$fid ORDER BY displayorder ASC, cid ASC");
    while($value = DB::fetch($query)) {
        $tree[] = array(
                'cid' => $value['cid'],
                'fid' => $value['fid'],
                'name' => $value['name'],
                'description' => $value['description'],
                'subcate' => get_categorytree($value[cid], $level, $ctype),
        );
    }
    
    return $tree;
}
function init_category($categoryArr, $cid = "", $level = 0, $offset = 1, $invalid_count = 2) {
    $level++;
    $html = "";

    foreach ($categoryArr as $value) {
        if($offset == 1 && $level <= $invalid_count) {
            $extattr = "disabled='disabled' style='color:#000;'";
        } else {
            $extattr = "";
        }
        $selected = $value[cid] == $cid ? "selected='selected'" : "";
        $html .= "<option value='$value[cid]' $selected $extattr>".str_repeat("&nbsp;", ($level-$offset)*4).$value[name]."</option>";
        $html .= init_category($value['subcate'], $cid, $level, $offset, $invalid_count);
    }

    return $html;
}
'''