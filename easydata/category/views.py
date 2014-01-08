from __future__ import unicode_literals

from django.shortcuts import render
from django.http import Http404, HttpResponseForbidden
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404
from django.utils.http import base36_to_int, int_to_base36
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import TemplateResponseMixin, View, RedirectView
from django.views.generic.edit import FormView, CreateView

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
from easydata.func.function_core import check_login, get_timestamp, elistdir
from pdf.uploads import handle_uploaded_file



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
import datetime
import time
from django.utils.timezone import now
from django.db import connection
from easydata.category.models import category
from easydata.category.forms import CategoryPostForm
from easydata.func.function_session import initial_form_session_for_custom_field,\
    clear_form_session_for_custom_field, set_form_session_for_custom_field
from account.views import DeleteView
from easydata.func.function_category import get_category_fid_choices_html,\
    get_category_list_html, get_categorytree


class CategoryPostView(FormView):
    template_name = 'category/post.html'
    form_class = CategoryPostForm
    action = 'new'
    category_instance = None 
    custom_field_css = None
    custom_field_errors = []
    
    def __init__(self, *args, **kwargs):
        super(CategoryPostView, self).__init__(*args, **kwargs)
    
    def get(self, *args, **kwargs):
        if not check_login(self.request) or self.request.user.is_superuser != True:
            return redirect("/account/login/")
        if 'pk' in self.kwargs and self.kwargs['pk'].isdigit():
            self.action = 'edit'
            self.category_instance = category.objects.get(pk=self.kwargs['pk'])
        initial_form_session_for_custom_field(CategoryPostForm, self.request.session)
        
        return super(CategoryPostView, self).get(*args, **kwargs)
    
    def get_initial(self):
        initial = super(CategoryPostView, self).get_initial()
        if self.action == 'edit':
            initial["name"] = self.category_instance.name
            CategoryPostForm.fid_choice_html = get_category_fid_choices_html(self.category_instance.fid)
            initial["description"] = self.category_instance.description
            initial["ctype"] = self.category_instance.ctype
            initial["displayorder"] = self.category_instance.displayorder
            initial["status"] = self.category_instance.status
        else:
            CategoryPostForm.fid_choice_html = get_category_fid_choices_html()
        return initial
    
    def get_context_data(self, **kwargs):
        context = super(CategoryPostView, self).get_context_data(**kwargs)
        if self.action == 'edit':
            context['head_title_text'] = _('Category Edit')
        else:
            context['head_title_text'] = _('New Category')
        return context
    
    def post(self, *args, **kwargs):
        if 'pk' in self.kwargs and self.kwargs['pk'].isdigit():
            self.action = 'edit'
            self.category_instance = category.objects.get(pk=self.kwargs['pk'])
        return super(CategoryPostView, self).post(*args, **kwargs)
    
    def form_valid(self, form):
        if not check_login(self.request) or self.request.user.is_superuser != True:
            return redirect("/account/login/")
        else:
            if self.request.POST['fid'] and self.request.POST['fid'].isdigit():
                cleaned_fid = self.request.POST['fid']
                clear_form_session_for_custom_field(self.request.session)
            else:
                set_form_session_for_custom_field(css={'fid': "has-error"}, text={'fid': ["Invalid father category input"]}, session=self.request.session)
                return redirect(self.request.path)
            
            
            if self.action == 'new':
                cate = category()
                cate.fid = cleaned_fid
                cate.name = form.cleaned_data.get("name")
                cate.description = form.cleaned_data.get("description")
                cate.status = form.cleaned_data.get("status")
                cate.displayorder = form.cleaned_data.get("displayorder")
                cate.ctype = form.cleaned_data.get("ctype")
                cate.save()
            else:
                self.category_instance.fid = cleaned_fid
                self.category_instance.name = form.cleaned_data.get("name")
                self.category_instance.description = form.cleaned_data.get("description")
                self.category_instance.status = form.cleaned_data.get("status")
                self.category_instance.displayorder = form.cleaned_data.get("displayorder")
                self.category_instance.ctype = form.cleaned_data.get("ctype")
                self.category_instance.save()
            
            return redirect(self.request.path)
            
            
        
    
    
    
class CategoryListView(TemplateView):
    model = category
    template_name = 'category/list.html'
    
    
    
    
    
    #def get_queryset(self):
    #    return category.objects.raw('SELECT * FROM `category_category` WHERE status>0 ORDER by id DESC')
        
        
    
    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['category_list'] = get_categorytree()
        #print context
        context['category_list_html'] = get_category_list_html() 
        context['head_title_text'] = _('Category List')
        #print context['category_list_html']
        return context

class CategoryDeleteView(RedirectView):
    url = '/category/'
    def get(self, *args, **kwargs):
        print 'fdsfdasf'
        return super(CategoryDeleteView, self).get(*args, **kwargs)
    
def CategoryDelete(request, pk):
    category.objects.get(pk=pk).delete()
    return HttpResponse('')


