from easydata.settings import cursor
from easydata.func.function_db import dictfetchall




def get_category_list():
    #cursor = connection.cursor()
    cursor.execute("SELECT id,fid,catename FROM `category_category` WHERE status>0 ORDER by id ASC")
    categorys = dictfetchall(cursor)
    return categorys
def get_category_fid_choices_html(cid=0):
    categorytree = get_categorytree()
    categorytree_merge = get_categorytree_merge(categorytree)
    html = "<option value='0'>None</option>"
    html += get_category_choices_html(categorytree_merge, cid, 0, 0)
    return html

def get_choices_html(cid=0,ctype=''):
    if not ctype:
        return ''
    categorytree = get_categorytree(ctype=ctype)
    html = get_category_choices_html(categorytree, cid, 0, 1)
    return html


def get_categorytree(fid=0,level=0,ctype=''):
    tree = {}
    level+=1
    if ctype == '':
        cursor.execute("SELECT ctype FROM `category_category` WHERE status>=0 GROUP BY ctype")
        result = dictfetchall(cursor)
        for value in result:
            tree[value['ctype']] = get_categorytree(0,0,value['ctype'])
        return tree
    
    cursor.execute("SELECT cid,fid,name,description FROM `category_category` WHERE status>0 AND ctype=%s AND fid=%s ORDER by displayorder DESC, cid ASC", (ctype, fid))
    result = dictfetchall(cursor)
    nodes = [] 
    for value in result:
        nodes.append(
            {'cid':value['cid'], 
             'fid':value['fid'], 
             'name':value['name'], 
             'description':value['description'], 
             'subcate':get_categorytree(int(value['cid']),level,ctype)})
    return nodes
 
def get_categorytree_merge(categorytree):
    x = []
    for k in categorytree:
        x.extend(categorytree[k])
    return x

def get_category_choices_html(categorys, cid = 0, level = 0, offset = 1, invalid_count = 0):
    level+=1
    html = "";
    
    for value in categorys:
        if level <= invalid_count:
            extattr = "disabled='disabled' style='color:#000;'";
        else:
            extattr = ""
        selected = "selected='selected'" if value['cid'] == cid  else "";
        html += "<option value='"+str(value['cid'])+"' "+selected+" "+extattr+">"+"&nbsp;"*((level-offset)*4)+value['name']+"</option>";
        html += get_category_choices_html(value['subcate'],cid,level,offset,invalid_count)
    return html


