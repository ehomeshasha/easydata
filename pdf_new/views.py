from django.shortcuts import render, redirect
#from django.views.generic import DetailView
from account.utils import default_redirect
import os
from easydata import settings
from pyquery import PyQuery as pq
from lxml import etree
import urllib
#from django.views import generic
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
import codecs
# Create your views here.


class PDF2HTMLView(TemplateView):
    #pass
    #def get_queryset(self):
    #    """Return the last five published polls."""
    #    return User.objects.get(pk=1)
    template_name = "pdf_new/view.html"
    
    #def get(self, *args, **kwargs):
        
        
        
        #print os.listdir(html_path)
    #    return super(PDF2HTMLView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        
        context = super(PDF2HTMLView, self).get_context_data(**kwargs)
        directory = "pdf_new/static/pdf_new/pdf2html/ehomeshasha/Data_Structure_And_Algorithms_In_Java/"
        filename = "pg_"+kwargs['id'].zfill(4)+".htm"
        filename2 = "pg_"+kwargs['id'].zfill(4)+"_new.htm"
        oripath = directory+filename
        oripath_abs=os.path.join(settings.PROJECT_ROOT, oripath)
        newpath = directory+filename2
        newpath_abs = os.path.join(settings.PROJECT_ROOT, newpath)
        
        if None:
            out = codecs.open(newpath_abs, 'r', "utf-8")
            content = out.read()
            out.close()
            pass
        else:
            ori_html = pq(filename=oripath_abs)
            background_img = ori_html('div').items().next().children('img')
            
            src = background_img.attr("src")
            background_img.attr("src", "/site_media/static/pdf_new/pdf2html/ehomeshasha/Data_Structure_And_Algorithms_In_Java/"+src) 
            height = background_img.attr("height")
            width = background_img.attr("width")
            new_html = pq('<div class="html_body" style="width:'+width+'px;height:'+height+'px;margin:0 auto;position:relative;"></div>')
            csss = ori_html('style')
            divs = ori_html('div')
            
            for css in csss.items():
                css_text = css.html().replace("<!--", "").replace("-->", "")
                if ".ft0" in css_text:
                    new_html.append('<style type="text/css">'+css_text+'</style>')
                    break
                
            for div in divs.items():
                css_string = div.attr('style')
                style=self.getDictFromCSSString(css_string)
                top = style['top']
                left = style['left']
                child_span = div.children('span')
                
                if child_span:
                    class_text = child_span.attr("class")
                    new_html.append(u'<div class="left-side side_bar" style="position:absolute;top:'+top+'px;left:-20px;width:20px;">\
                                        <a class="'+class_text+' side_link">&nbsp;</a>\
                                    </div>\
                                    <div class="middle-content" style="position:absolute;top:'+top+'px;left:'+left+'px;">'
                                    +div.html()+
                                    u'</div>\
                                    <div class="right-side side_bar" style="position:absolute;top:'+top+'px;left:826px;width:20px;">\
                                        <a class="'+class_text+' side_link">&nbsp;</a>\
                                    </div>')
                else:
                    new_html.append(div.outerHtml())
                
                
            content = new_html.outerHtml()
            out = codecs.open(newpath_abs, 'wb', "utf-8")
            out.write(content)
            out.close()
        
        
            
        context['pdf_content'] = content 
        #print content
        return context
#class DetailView(generic.DetailView):
    #model = Poll
#    template_name = 'polls/detail.html'   
    
    
    def getDictFromCSSString(self, css_string):
        return dict((name.strip(), val.strip()) for name, val in (pair.split(':') for pair in css_string.split(';')))
    
    


