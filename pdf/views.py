from __future__ import unicode_literals

from django.shortcuts import render
from django.http import Http404, HttpResponseForbidden
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404
from django.utils.http import base36_to_int, int_to_base36
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.edit import FormView

from account.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.sites.models import get_current_site
from django.contrib.auth.tokens import default_token_generator
from pdf.forms import PDFUploadForm
from django.http.response import HttpResponseRedirect, HttpResponse
# Create your views here.
import json

from pdf.models import pdf as pdfModel
from easydata.func.function_core import check_login
from pdf.uploads import handle_uploaded_file
from easydata.constant import TIMESTAMP


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
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

class PDFUploadView(FormView):
    template_name = "pdf/upload.html"
    form_class = PDFUploadForm
    model = pdfModel
    
    def __init__(self, *args, **kwargs):
        #self.created_user = None
        #kwargs["signup_code"] = None
        super(PDFUploadView, self).__init__(*args, **kwargs)
        
    

    def get(self, *args, **kwargs):
        if not check_login(self.request):
            return redirect("/account/login/")
        return super(PDFUploadView, self).get(*args, **kwargs)
    
    
    def form_valid(self, form):
        if not check_login(self.request):
            return redirect("/account/login/")
        else:
            self.User = self.request.user
        #upload pdf to server
        filepath = handle_uploaded_file(self.request.FILES['store_file'], self.User.username)
        #save information about uploading to database
        self.pdf_save(form, commit=True, filepath=filepath)
        return HttpResponse('');
        
    def pdf_save(self, form, commit=True, **kwargs):
        
        pdf = pdfModel()
        pdf.title = form.cleaned_data.get("title")
        pdf.description = form.cleaned_data.get("description")
        pdf.uid = self.User.id
        pdf.username = self.User.username
        pdf.filepath = kwargs['filepath']
        pdf.filename = self.request.FILES['store_file']._name
        pdf.dateline = TIMESTAMP
        
        if commit:
            pdf.save()
        
        



class PDF2HTMLView(DetailView):
    #pass
    #def get_queryset(self):
    #    """Return the last five published polls."""
    #    return User.objects.get(pk=1)
    model = pdfModel
    template_name = "pdf/view.html"
    
    #def get(self, *args, **kwargs):
        
        
        
        #print os.listdir(html_path)
    #    return super(PDF2HTMLView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PDF2HTMLView, self).get_context_data(**kwargs)
        #print context['object'].filepath
        #print context['object'].filename
        #print self.kwargs['page_num']
        book_dir = os.path.dirname(os.path.dirname(context['object'].filepath[1:]))
        #pdf/static/pdf/pdf2html/zzy2/Hadoop_in_Action
        origin_dir = os.path.join(book_dir, 'origin/')
        image_dir = "/"+origin_dir
        new_dir = os.path.join(book_dir, 'new/')
        #directory = "pdf/static/pdf/pdf2html/ehomeshasha/Data_Structure_And_Algorithms_In_Java/"
        filename = "pg_"+self.kwargs['page_num'].zfill(4)+".htm"
        #filename2 = "pg_"+kwargs['page_num'].zfill(4)+"_new.htm"
        oripath = origin_dir+filename
        oripath_abs=os.path.join(settings.PROJECT_ROOT, oripath)
        newpath = new_dir+filename
        newpath_abs = os.path.join(settings.PROJECT_ROOT, newpath)
        
        if not settings.DEBUG and os.path.exists(newpath_abs):
            out = codecs.open(newpath_abs, 'r', "utf-8")
            content = out.read()
            out.close()
            pass
        else:
            ori_html = pq(filename=oripath_abs)
            background_img = ori_html('div').items().next().children('img')
            
            src = background_img.attr("src")
            background_img.attr("src", image_dir+src) 
            height = background_img.attr("height")
            width = background_img.attr("width")
            new_html = pq('<div class="pdf_wrapper" style="width:'+width+'px;height:'+height+'px;margin:0 auto;position:relative;"></div>')
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
    
    
    def getDictFromCSSString(self, css_string):
        return dict((name.strip(), val.strip()) for name, val in (pair.split(':') for pair in css_string.split(';')))
    
    
    
class PDFListView(ListView):
    model = pdfModel
    template_name = "pdf/list.html"
    
    pass