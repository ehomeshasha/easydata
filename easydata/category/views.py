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


class CategoryPostView(FormView):
    model = category
    template_name = 'category/post.html'
    form_class = CategoryPostForm
    
    def get(self, *args, **kwargs):
        if not check_login(self.request) or self.request.user.is_superuser != True:
            return redirect("/account/login/")
        return super(CategoryPostView, self).get(*args, **kwargs)
    
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
        pdf.filesize = self.request.FILES['store_file']._size
        pdf.date_upload = now() 
        
        if commit:
            pdf.save()
    
    
class CategoryListView(ListView):
    model = category
    template_name = 'category/list.html'
    
class CategoryDeleteView(View):
    model = category
    