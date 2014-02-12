from django import template
from django.utils.timezone import now
from code.syntaxhighlighter import Syntaxhighlighter
import re
from easydata.constant import LANGUAGE_DICT
from code.models import Code
from article.models import Article
from easydata.category.models import category
register = template.Library()
from django.utils.translation import ugettext as _
@register.filter()
def hdate(value):
    if not value:
        return ""
    
    timedelta = now() - value

    days = int(timedelta.days)
    seconds = int(timedelta.seconds)
    if days < 1:
        if seconds>3600:
            return str(int(seconds/3600))+_(" hours ago");
        elif seconds>1800:
            return _("half hour ago");
        elif seconds>60:
            return str(int(seconds/60))+_(" minutes ago");
        elif seconds>0:
            return str(seconds)+_(" seconds ago");
        elif seconds==0:
            return 'just now'
    elif days == 1:
        return _("yesterday")
    elif days < 7:
        return str(days)+_(" days ago")
    else:
        return template.defaultfilters.date(value, "SHORT_DATE_FORMAT")


@register.filter()
def hsize(size):
    num = int(size)
    for x in ['bytes','KB','MB','GB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')

@register.filter()
def get_category_name(pk):
    return category.objects.get(pk=pk).name


@register.filter()
def cate_id_format(cate_id, category_dict_pk):
    try:
        ids = [cate_id]
        recursive_cate_id_format(cate_id, ids, category_dict_pk)
        ids.reverse()
        html = "<ul>"
        for v in ids:
            html += "<li>%s</li><ul>" % category_dict_pk[v]['name']
            
        html += "</ul>"*(len(ids)+1)
        return html
    except:
        return ''
    
def recursive_cate_id_format(cate_id, ids, category_dict_pk):
    if cate_id == 0:
        return
    fid = category_dict_pk[cate_id]['fid']
    if fid == 0:
        return
    ids.append(fid)
    recursive_cate_id_format(fid, ids, category_dict_pk)
    

@register.assignment_tag
def get_auth_author_admin(authorid, uid, is_superuser):
    if uid and (is_superuser or authorid == id):
        return True
    return False

@register.filter()   
def get_active_class(path, path_start):
    if path.startswith(path_start):
        return 'active'
    return ''

@register.assignment_tag
def check_appname(path, app_name):
    if path.startswith(app_name):
        return True
    return False

@register.simple_tag
def get_code(pk):
    try:
        code_instance = Code.objects.get(pk=pk)
    except Code.DoesNotExist:
        return _('<code>Code (ID:%d) does not exist, please check</code>' % pk)
    hl = Syntaxhighlighter(code_instance)
    code = hl.get_code()
    return template.defaultfilters.safe(code)
    
@register.filter()
def get_dict_value(key, dictionary):
    try:
        return dictionary[key]
    except KeyError:
        return ''
    
@register.filter()
def yes_or_no(value):
    if value==True or value==1 or value=='1':
        return _('Yes')
    elif value==False or value==0 or value == '0':
        return _('No')
    else:
        return ''
max_height_pattern = re.compile(r'max_height(\d+)')
@register.filter()
def max_height_convert(value):
    max_height_match = re.match(max_height_pattern, value)
    if max_height_match:
        return "%spx" % max_height_match.group(1)
    else:
        return ''
    
@register.filter()  
def get_language_shortname(language_code):
    try:
        return LANGUAGE_DICT[language_code]['shortname']
    except KeyError:
        return ''
    
code_pattern = re.compile(r'{%\s*get_code\s*(\d+)\s*%}')
@register.filter()
def get_code_detail_from_content(content):
    matches = re.finditer(code_pattern, content)
    if matches:
        html = "<ul class='no-margin plw prm'>"
        for m in matches:
            code = Code.objects.get(pk=int(m.group(1)))
            html += "<li><a title='%s' href='/code/view/%d' class=''>%s</a></li>" % (code.description, code.id,code.title) 
        html += "</ul>"
    return template.defaultfilters.safe(html)
        
@register.simple_tag 
def get_articles(articleindex_id):
    articles = Article.objects.filter(fid=articleindex_id, displayorder__gte=0)
    html = "<ul class='no-margin plw prm'>"
    for article in articles:
        html += "<li><a href='/article/view/%d/'>%s</a></li>" % (article.id, article.title[:60])
    html += "</ul>"
    return template.defaultfilters.safe(html)