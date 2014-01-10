from __future__ import unicode_literals

from django.shortcuts import redirect, render
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import FormView

from pdf.forms import PDFUploadForm

from pdf.models import pdf as pdfModel
from easydata.func.function_core import check_login, elistdir, multi, page_jump
from pdf.uploads import handle_uploaded_file

import os
from easydata import settings
from pyquery import PyQuery as pq  # @UnresolvedImport

import codecs
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from django.utils.timezone import now
from easydata.func.function_session import initial_form_session_for_custom_field,\
    clear_form_session_for_custom_field, set_form_session_for_custom_field
from easydata.func.function_category import get_choices_html, get_category_dict_pk
from django.contrib import messages
from easydata.settings import PROJECT_ROOT
from django.http.response import HttpResponse
from easydata.constant import CONTENT_TYPE, HOME_BREAD
from django.db import connection

def update_convert_status(pdf, **kwargs):
    if 'list' in kwargs.keys() and kwargs['list']:
        for p in pdf:
            if p.isconvert == '1':
                continue
            update_convert_status(p, check_exists=kwargs['check_exists'])
    else:
        if pdf.isconvert == '1':
            return;
        cursor = connection.cursor();
        if 'check_exists' in kwargs.keys() and kwargs['check_exists']:
            book_dir = os.path.dirname(os.path.dirname(pdf.filepath[1:]))
            origin_dir = os.path.join(book_dir, 'origin/')
            if elistdir(origin_dir, 'file'):
                cursor.execute("UPDATE `pdf_pdf` SET `isconvert`=%s WHERE `id`='%s'", [1,pdf.id])
        else:
            cursor.execute("UPDATE pdf_pdf SET isconvert=%s WHERE id='%s'", [1,pdf.id])
    

class PDFUploadView(FormView):
    template_name = "pdf/upload.html"
    form_class = PDFUploadForm
    
    action = 'new'
    pdf_instance = None 
    
    def __init__(self, *args, **kwargs):
        self.breadcrumb = [HOME_BREAD,{'text': 'PDF','href': '/pdf/list/'},] 
        super(PDFUploadView, self).__init__(*args, **kwargs)
        
    def get(self, *args, **kwargs):
        if not check_login(self.request):
            return redirect("/account/login/?next=%s" % self.request.path)
        if 'pk' in self.kwargs and self.kwargs['pk'].isdigit():
            self.action = 'edit'
            self.pdf_instance = pdfModel.objects.get(pk=self.kwargs['pk'])
        
        initial_form_session_for_custom_field(PDFUploadForm, self.request.session)
        
        return super(PDFUploadView, self).get(*args, **kwargs)
    
    def get_initial(self):
        initial = super(PDFUploadView, self).get_initial()
        if self.action == 'edit':
            initial["title"] = self.pdf_instance.title
            PDFUploadForm.choice_html = get_choices_html(cid=self.pdf_instance.cate_id,ctype='pdf')
            initial["description"] = self.pdf_instance.description
        else:
            PDFUploadForm.choice_html = get_choices_html(cid=0,ctype='pdf')
        return initial
    
    def get_context_data(self, **kwargs):
        context = super(PDFUploadView, self).get_context_data(**kwargs)
        if self.action == 'edit':
            context['head_title_text'] = _('PDF Edit')
            context['legend_text'] = _('PDF Edit')
            context['submit_btn_text'] = _('Submit')
            self.breadcrumb.append({'text': 'Edit'})
        else:
            context['head_title_text'] = _('PDF Upload')
            context['legend_text'] = _('PDF Upload')
            context['submit_btn_text'] = _('Upload')
            self.breadcrumb.append({'text': 'Upload'})
        context['breadcrumb'] = self.breadcrumb
        
        return context
    
    def post(self, *args, **kwargs):
        if not check_login(self.request):
            return redirect("/account/login/?next=%s" % self.request.path)
        if 'pk' in self.kwargs and self.kwargs['pk'].isdigit():
            self.action = 'edit'
            self.pdf_instance = pdfModel.objects.get(pk=self.kwargs['pk'])
            
        return super(PDFUploadView, self).post(*args, **kwargs)
    
    def get_form(self, form_class):
        instance = form_class(**self.get_form_kwargs())
        if self.action == 'edit':
            instance.fields.pop('store_file')
        return instance
    
    def form_valid(self, form):
        
        self.User = self.request.user
        if self.request.POST['cate_id'] and self.request.POST['cate_id'].isdigit():
            cleaned_cate_id = self.request.POST['cate_id']
            clear_form_session_for_custom_field(self.request.session)
        else:
            set_form_session_for_custom_field(css={'cate_id': "has-error"}, text={'cate_id': ["Invalid category input"]}, session=self.request.session)
            return redirect(self.request.path)
        
        if self.action == 'new':
            #upload pdf to server
            filepath = handle_uploaded_file(self.request.FILES['store_file'], self.User.username)
            #save information about uploading to database
            self.pdf_save(form, commit=True, filepath=filepath, cate_id=cleaned_cate_id)
            message_body = _('PDF has been successfully uploaded')
        else:
            #update pdf information
            self.pdf_update(form, commit=True, cate_id=cleaned_cate_id)
            message_body = _('Information about this PDF has been successfully modified')
        
        messages.success(self.request, message_body)
        return redirect('/pdf/list/');
        
    def pdf_save(self, form, commit=True, **kwargs):
        pdf = pdfModel()
        pdf.title = form.cleaned_data.get("title")
        pdf.description = form.cleaned_data.get("description")
        pdf.uid = self.User.id
        pdf.username = self.User.username
        pdf.cate_id = kwargs['cate_id']
        pdf.filepath = kwargs['filepath']
        pdf.filename = self.request.FILES['store_file']._name
        pdf.filesize = self.request.FILES['store_file']._size
        pdf.date_upload = now() 
        
        if commit:
            pdf.save()

    def pdf_update(self, form, commit=True, **kwargs):
        pdf = self.pdf_instance
        pdf.title = form.cleaned_data.get("title")
        pdf.cate_id = kwargs['cate_id']
        pdf.description = form.cleaned_data.get("description")
        if commit:
            pdf.save()
    

class PDF2HTMLView(DetailView):
    model = pdfModel
    template_name = "pdf/view.html"
    sidebar_width = 35 
    
    def __init__(self, *args, **kwargs):
        self.breadcrumb = [HOME_BREAD,{'text': 'PDF','href': '/pdf/list/'},] 
        super(PDF2HTMLView, self).__init__(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(PDF2HTMLView, self).get_context_data(**kwargs)
        context['head_title_text'] = _('PDF Detail')
        self.breadcrumb.append({'text': 'Detail'})
        
        book_dir = os.path.dirname(os.path.dirname(context['pdf'].filepath[1:]))
        origin_dir = os.path.join(book_dir, 'origin/')
        filepn = len(elistdir(origin_dir, 'file', '.jpg'))
        if filepn:
            update_convert_status(context['pdf']);
            
            image_dir = "/"+origin_dir
            new_dir = os.path.join(book_dir, 'new/')
            if not self.kwargs['page_num']:
                self.kwargs['page_num'] = '1'
            curpage = int(self.kwargs['page_num'])
            filename = "pg_%s.htm" % self.kwargs['page_num'].zfill(4)
            oripath = origin_dir+filename
            oripath_abs=os.path.join(settings.PROJECT_ROOT, oripath)
            newpath = new_dir+filename
            newpath_abs = os.path.join(settings.PROJECT_ROOT, newpath)
            
            #if not settings.DEBUG and os.path.exists(newpath_abs):
            if None:
                out = codecs.open(newpath_abs, 'r', "utf-8")
                content = out.read()
                out.close()
                pass
            else:
                ori_html = pq(filename=oripath_abs)
                background_img = ori_html('div').items().next().children('img')
                
                src = background_img.attr("src")
                background_img.attr("src", image_dir+src) 
                height = int(background_img.attr("height"))
                width = int(background_img.attr("width"))
                new_html = pq('<div class="pdf_wrapper" style="width:%dpx;height:%dpx;margin:0 auto;position:relative;"></div>' % (width,height))
                csss = ori_html('style')
                divs = ori_html('div')
                row_width = width+self.sidebar_width*2
                
                for css in csss.items():
                    css_text = css.html().replace("<!--", "").replace("-->", "")
                    if ".ft0" in css_text:
                        new_html.append('<style type="text/css">%s</style>' % css_text)
                        break
                    
                for k,div in enumerate(divs.items()):
                    css_string = div.attr('style')
                    style=self.getDictFromCSSString(css_string)
                    top = style['top']
                    left = style['left']
                    child_span = div.children('span')
                    
                    if child_span:
                        class_text = child_span.attr("class")
                        new_html.append(u'<div data-num="%d" class="left-side side_bar" style="position:absolute;top:%spx;left:%dpx;width:%dpx;z-index:8">\
                                            <a class="%s side_link">&nbsp;</a>\
                                        </div>\
                                        <div  data-num="%d"  class="row_layer" style="position:absolute;top:%spx;left:%dpx;width:%dpx;z-index:9">\
                                            <div class="row_layer_content">&nbsp;</div>\
                                        </div>\
                                        <div  data-num="%d" class="middle-content" style="position:absolute;top:%spx;left:%spx;z-index:1">%s</div>' 
                                        % (k, top, -self.sidebar_width, self.sidebar_width, class_text,
                                           k, top, -self.sidebar_width, row_width, 
                                           k, top, left, div.html()))
                    else:
                        new_html.append(div.outerHtml())
                    
                    
                content = new_html.outerHtml()
                out = codecs.open(newpath_abs, 'wb', "utf-8")
                out.write(content)
                out.close()
            
            
                
            context['pdf_content'] = content
            context['breadcrumb'] = self.breadcrumb
            
            if not context['pdf'].filepn:
                cursor = connection.cursor()
                cursor.execute("UPDATE pdf_pdf SET filepn = %s WHERE id = %s", [filepn, context['pdf'].id])
            context['page_jump'] = page_jump(pn=filepn, curpage=curpage, mpurl='/pdf/view/%d/' % context['pdf'].id)
            #context['filepn'] = filepn
            print filepn
            #print pdf_pagination
        else:
            pass
        
        return context
    
    def getDictFromCSSString(self, css_string):
        return dict((name.strip(), val.strip()) for name, val in (pair.split(':') for pair in css_string.split(';')))
    
    

    
class PDFListView(ListView):
    model = pdfModel
    template_name = "pdf/list.html"
    
    def __init__(self, *args, **kwargs):
        self.breadcrumb = [HOME_BREAD,{'text': 'PDF'},] 
        super(PDFListView, self).__init__(*args, **kwargs)
    
    def get_queryset(self):
        return pdfModel.objects.raw('SELECT * FROM `pdf_pdf` WHERE displayorder>=0 ORDER by date_upload DESC')
    
    def get_context_data(self, **kwargs):
        context = super(PDFListView, self).get_context_data(**kwargs)
        context['head_title_text'] = _('PDF List')
        context['breadcrumb'] = self.breadcrumb
        context['category_dict_pk'] = get_category_dict_pk()
        return context 

def download_pdf(request, pk):
    pdf = pdfModel.objects.get(pk=pk)
    pdf_path = os.path.join(PROJECT_ROOT, pdf.filepath[1:])
    fsock = open(pdf_path, 'r')
    response = HttpResponse(fsock, mimetype=CONTENT_TYPE['pdf'])
    response['Content-Disposition'] = "attachment; filename=%s" % pdf.filename 
    return response

def delete_pdf(request, pk):
    pdf = pdfModel.objects.get(pk=pk)
    pdf.delete()
    message_body = "Title:%s has been deleted" % pdf.title
    messages.success(request, message_body)
    return HttpResponse('')

def mark_pdf(request,action, pk, page_num, line_num):
    modal_form = {
        'javascript': '',
        'form_action': '',
        'title': 'Mark line',
        'hid_input': None,
        'btn_primary': _("Submit"),
        'btn_default': _("Close"),
    }
    context = {
        'action': action,
        'pk': pk,
        'page_num': page_num,
        'line_num': line_num,
        'modal_form': modal_form
    }
    return render(request, 'pdf/mark.html', context)
    
    
    
    