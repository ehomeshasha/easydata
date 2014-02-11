from __future__ import division
from os import listdir
from os.path import isfile, join
from django.contrib import messages
import time
from django.utils.timezone import now
import math
from django.core.paginator import Paginator

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

def elistdir(directory, find_type='all', suffix = ''):
    if find_type == 'all':
        return [ f for f in listdir(directory)]
    elif find_type =='file':
        return [ f for f in listdir(directory) if isfile(join(directory,f)) and (suffix == '' or (suffix != '' and f.endswith(suffix))) ]
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


def get_auth_author_admin(user, authorid):
    if user and (user.id == authorid or user.is_superuser == 1):
        return True
    return False


def get_add_icon(href,tooltip):
    return {'text':'+', 'href':href, 'tooltip':tooltip, 'is_label':1}


def multi(num, perpage, curpage, mpurl, maxpages = 0, page = 10, autogoto = False, simple = False):
    prev_txt = "&lsaquo;";
    next_txt = "&rsaquo;";                                                                                                           
    dot = '...';
    multipage = '';

    realpages = 1;
    page -= len(str(curpage)) - 1
    if page <= 0:
        page = 1
    
    if num > perpage:

        offset = int(math.floor(page * 0.5))  # @UndefinedVariable

        realpages = int(math.ceil(num/perpage))  # @UndefinedVariable
        if maxpages and maxpages < realpages:
            pages = maxpages
        else:
            pages = realpages
        if page > pages:
            fromm = 1
            to = pages
        else:
            fromm = curpage - offset
            to = fromm + page - 1
            if fromm < 1:
                to = curpage + 1 - fromm
                fromm = 1;
                if to - fromm < page:
                    to = page
            elif to > pages:
                fromm = pages - page + 1
                to = pages
        if curpage - offset > 1 and pages > page:
            multipage = '<li><a onclick=\'jumpto("%s1/");\' href="javascript:;">1 %s</a></li>' % (mpurl, dot) 
        else:
            multipage = ''
        if curpage > 1 and not simple :
            multipage += '<li><a onclick=\'jumpto("%s%d/");\' href="javascript:;">%s</a></li>' % (mpurl, curpage-1, prev_txt)
        else:
            multipage += '<li class="disabled"><a href="javascript:;">%s</a></li>' % prev_txt
        for i in range(fromm, to+1):
            if i == curpage:
                multipage += '<li class="active"><a href="javascript:;">%d</a></li>' % i
            else:
                multipage += '<li><a onclick=\'jumpto("%s%d/");\' href="javascript:;">%d</a></li>' % (mpurl, i, i);
        if to < pages:
            multipage += '<li><a onclick=\'jumpto("%s%d/");\' href="javascript:;">%s %d</a></li>' % (mpurl, pages, dot, realpages)
        else:
            multipage += ''
        if curpage < pages and not simple:
            multipage += '<li><a onclick=\'jumpto("%s%d/");\' href="javascript:;">%s</a></li>' % (mpurl, curpage+1, next_txt)
        else:
            multipage += '<li class="disabled"><a href="javascript:;">%s</a></li>' % next_txt
        if multipage:
            multipage = '<ul class="pagination">%s</ul>' % multipage
        else:
            multipage = ''
    return multipage

def page_jump(pn,curpage):
    prev_class = next_class = ''
    prev_num = curpage - 1
    next_num = curpage + 1
    if curpage == 1:
        prev_class = 'disabled'
    if curpage == pn:
        next_class = 'disabled'
    
        
    
    html = '<a href="javascript:;" class="prev_btn btn btn-default btn-xs %s" data-num="%d">&lsaquo;</a>\
            <span class="btn btn-default pn_input_area btn-xs">\
                <input type="text" class="pn_input col-md-6" value="%d" maxlength="5" />\
                <span class="maxpn">/%d</span>\
            </span>\
            <a href="javascript:;" class="next_btn btn btn-default btn-xs %s" data-num="%d">&rsaquo;</a>\
            ' % (prev_class, prev_num, curpage, pn, next_class, next_num)
    return html

def get_curpage(page, maxpage):
    if not page or not page.isdigit():
        return 1
    elif int(page) > maxpage:
        return maxpage
    else:
        return int(page)
    
def get_pagination_from_rawqueryset(context, perpage):
    
    object_list = list(context['object_list']) 
    p = Paginator(object_list,perpage)
    curpage = get_curpage(context['view'].request.GET.get('page'), p.num_pages)
    cur_paginator = p.page(curpage)
    return cur_paginator.object_list, cur_paginator, p.num_pages-1 
    
    