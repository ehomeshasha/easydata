# -*- coding: utf-8 -*-  
from __future__ import unicode_literals

from django.shortcuts import redirect, render
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import FormView

from pdf.forms import PDFUploadForm, PDFCommentForm

from pdf.models import pdf as pdfModel, Mark, Comment
from easydata.func.function_core import check_login, elistdir, page_jump,\
    get_add_icon, showmessage, download
from pdf.uploads import handle_uploaded_file

import os
from easydata import settings
from pyquery import PyQuery as pq  # @UnresolvedImport

import codecs
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from django.utils.timezone import now
from easydata.func.function_session import initial_form_session_for_custom_field,\
    clear_form_session
from easydata.func.function_category import get_choices_html, get_category_dict_pk
from django.contrib import messages
from easydata.settings import PROJECT_ROOT
from django.http.response import HttpResponse
from easydata.constant import CONTENT_TYPE, HOME_BREAD, PERPAGE,\
    PERMISSION_ERROR
from easydata.validator import CharValidator, IntegerValidator, \
    save_cleaned_data
from easydata.templatetags.custom_tags import get_auth_author_admin

def update_convert_status(pdf, **kwargs):
    if 'list' in kwargs.keys() and kwargs['list']:
        for p in pdf:
            if p.isconvert == True:
                continue
            update_convert_status(p, check_exists=kwargs['check_exists'])
    else:
        if pdf.isconvert == True:
            return;
        if 'check_exists' in kwargs.keys() and kwargs['check_exists']:
            book_dir = os.path.dirname(os.path.dirname(pdf.filepath[1:]))
            origin_dir = os.path.join(book_dir, 'origin/')
            if elistdir(origin_dir, 'file'):
                pdf.isconvert = True
                pdf.save()
        else:
            pdf.isconvert = True
            pdf.save
    

class PDFUploadView(FormView):
    template_name = "pdf/upload.html"
    form_class = PDFUploadForm
    
    action = 'new'
    pdf_instance = None 
    
    def __init__(self, *args, **kwargs):
        self.breadcrumb = [HOME_BREAD,{'text': _('PDF'),'href': '/pdf/list/'},] 
        super(PDFUploadView, self).__init__(*args, **kwargs)
        
    def get(self, *args, **kwargs):
        
        if not check_login(self.request):
            return redirect("/account/login/?next=%s" % self.request.get_full_path())
        if 'pk' in self.kwargs and self.kwargs['pk'].isdigit():
            self.action = 'edit'
            self.pdf_instance = pdfModel.objects.get(pk=self.kwargs['pk'])
        
            if not get_auth_author_admin(self.pdf_instance.uid, self.request.user.id, self.request.user.is_superuser):
                return showmessage(self.request, PERMISSION_ERROR)
        
        return super(PDFUploadView, self).get(*args, **kwargs)
    
    def get_initial(self):
        initial = super(PDFUploadView, self).get_initial()
        if self.action == 'edit':
            initial["title"] = self.pdf_instance.title
            initial["description"] = self.pdf_instance.description
        
        return initial
    
    def get_context_data(self, **kwargs):
        context = super(PDFUploadView, self).get_context_data(**kwargs)
        if self.action == 'edit':
            context['head_title_text'] = _('PDF Edit')
            context['legend_text'] = _('PDF Edit')
            context['submit_btn_text'] = _('Submit')
            self.breadcrumb.append({'text': 'Edit'})
            context['form'].choice_html = get_choices_html(cid=self.pdf_instance.cate_id,ctype='pdf')
        else:
            context['head_title_text'] = _('PDF Upload')
            context['legend_text'] = _('PDF Upload')
            context['submit_btn_text'] = _('Upload')
            self.breadcrumb.append({'text': 'Upload'})
            context['form'].choice_html = get_choices_html(cid=0,ctype='pdf')
        
        context['breadcrumb'] = self.breadcrumb
        initial_form_session_for_custom_field(context['form'], self.request.session)
        
        return context
    
    def post(self, *args, **kwargs):
        if not check_login(self.request):
            return redirect("/account/login/?next=%s" % self.request.get_full_path())
        if 'pk' in self.kwargs and self.kwargs['pk'].isdigit():
            self.action = 'edit'
            self.pdf_instance = pdfModel.objects.get(pk=self.kwargs['pk'])
            
            if not get_auth_author_admin(self.pdf_instance.uid, self.request.user.id, self.request.user.is_superuser):
                return showmessage(self.request, PERMISSION_ERROR)
            
        return super(PDFUploadView, self).post(*args, **kwargs)
    
    def get_form(self, form_class):
        instance = form_class(**self.get_form_kwargs())
        if self.action == 'edit':
            instance.fields.pop('store_file')
        return instance
    
    def form_valid(self, form):
        
        self.User = self.request.user
        
        #validate cate_id
        cate_id_validator = IntegerValidator(validate_key='cate_id',
                                    validate_label='Category ID', 
                                    session=self.request.session, 
                                    post=self.request.POST)
        cate_id_validate_result = cate_id_validator.check()
        if cate_id_validate_result:
            cleaned_cate_id = cate_id_validator.get_value()
            clear_form_session(self.request.session)
        else:
            self.request.session.modified = True
            return redirect(self.request.get_full_path())
        
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
        self.breadcrumb = [HOME_BREAD,{'text': _('PDF'),'href': '/pdf/list/'},]
        
        super(PDF2HTMLView, self).__init__(*args, **kwargs)
    
    def get(self, *args, **kwargs):
        if 'ajax' in self.request.GET and self.request.GET['ajax'] == '1':
            self.template_name = "pdf/pdf_content.html" 
        return super(PDF2HTMLView, self).get(*args, **kwargs)    
    
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
            
            mark_count_for_this_page = Mark.objects.filter(page_num=self.kwargs['page_num']).count()
            
            if not settings.DEBUG and os.path.exists(newpath_abs):
            #if None:
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
                new_html = pq('<div id="pdf_wrapper" class="pdf_wrapper" style="width:%dpx;height:%dpx;margin:0 auto;position:relative;"></div>' % (width,height))
                csss = ori_html('style')
                divs = ori_html('div')
                row_width = width+self.sidebar_width*2
                
                for css in csss.items():
                    css_text = css.html().replace("<!--", "").replace("-->", "")
                    if ".ft0" in css_text:
                        new_html.append('<style type="text/css">%s</style>' % css_text)
                        break
               
                for k,div in enumerate(divs.items()):
                    anchor = '<a>&nbsp;</a>'
                    if mark_count_for_this_page:
                        mark_count_for_this_line = Mark.objects.filter(page_num=self.kwargs['page_num'], line_num=k).count()
                        if mark_count_for_this_line:
                            anchor = '<a href="javascript:;" class="mark_count" data-toggle="tooltip" data-trigger="manual" title="" data-placement="left" data-title="%d">&nbsp;</a>' % mark_count_for_this_line
                    
                    css_string = div.attr('style')
                    style=self.getDictFromCSSString(css_string)
                    top = style['top']
                    left = style['left']
                    child_span = div.children('span')
                    
                    if child_span:
                        class_text = child_span.attr("class")
                        new_html.append(u'<div data-num="%d" class="left-side side_bar" style="position:absolute;top:%spx;left:%dpx;width:%dpx;z-index:8">\
                                            %s\
                                        </div>\
                                        <div  data-num="%d"  class="row_layer" style="position:absolute;top:%spx;left:%dpx;width:%dpx;z-index:9">\
                                            <div class="%s row_layer_content">&nbsp;</div>\
                                        </div>\
                                        <div  data-num="%d" class="middle-content" style="position:absolute;top:%spx;left:%spx;z-index:1">%s</div>' 
                                        % (k, top, -self.sidebar_width, self.sidebar_width, anchor,
                                           k, top, -self.sidebar_width, row_width, class_text, 
                                           k, top, left, div.html()))
                    else:
                        new_html.append(div.outerHtml())
                    
                    
                content = new_html.outerHtml()
                out = codecs.open(newpath_abs, 'wb', "utf-8")
                out.write(content)
                out.close()
            
                
            context['pdf_content'] = content
            context['breadcrumb'] = self.breadcrumb
            context['page_jump'] = page_jump(pn=filepn, curpage=curpage)
            
            if not context['pdf'].filepn:
                context['pdf'].filepn = filepn
                #cursor = connection.cursor()
                #cursor.execute("UPDATE pdf_pdf SET filepn = %s WHERE id = %s", [filepn, context['pdf'].id])
            context['pdf'].views += 1     
            context['pdf'].save()
            
            #comment_box
            comment_list = Comment.objects.filter(pdf_id=context['pdf'].id, displayorder__gte=0).order_by("date_create")
            context['comment_list'] = comment_list
            
            
            
        else:
            pass
        return context
    
    def getDictFromCSSString(self, css_string):
        return dict((name.strip(), val.strip()) for name, val in (pair.split(':') for pair in css_string.split(';')))
    
    

    
class PDFListView(ListView):
    model = pdfModel
    template_name = "pdf/list.html"
    paginate_by = PERPAGE
    
    def __init__(self, *args, **kwargs):
        self.breadcrumb = [HOME_BREAD,{'text': _('PDF')},get_add_icon('/pdf/upload/',_('Upload PDF'))] 
        super(PDFListView, self).__init__(*args, **kwargs)
    
    def get_queryset(self):
        return pdfModel.objects.filter(displayorder__gte=0).order_by("-date_upload")
    
    def get_context_data(self, **kwargs):
        context = super(PDFListView, self).get_context_data(**kwargs)
        context['head_title_text'] = _('PDF List')
        context['breadcrumb'] = self.breadcrumb
        context['category_dict_pk'] = get_category_dict_pk()
        return context 

def download_pdf(request, pk):
    pdf = pdfModel.objects.get(pk=pk)
    pdf_path = pdf.filepath
    return download(pdf_path, filetype='pdf')

def delete_pdf(request, pk):
    pdf = pdfModel.objects.get(pk=pk)
    if not get_auth_author_admin(pdf.uid, request.user.id, request.user.is_superuser):
        return showmessage(request, PERMISSION_ERROR)
    pdf.delete()
    message_body = "PDF: %s has been deleted" % pdf.title
    messages.success(request, message_body)
    return HttpResponse('')



def get_mark_nav_href(pk, page_num, line_num):
    return {
        'post': '/pdf/mark_post/%s/%s/%s/' % (pk, page_num, line_num),
        'view_line': '/pdf/mark_view_line/%s/%s/%s/' % (pk, page_num, line_num),
        'view_page': '/pdf/mark_view_page/%s/%s/%s/' % (pk, page_num, line_num),
        'about': '/pdf/mark_about/%s/%s/%s/' % (pk, page_num, line_num),
    }

def mark_post(request, pk, page_num, line_num):
    
    if request.method == 'GET':
        modal_form = {
            'action': request.get_full_path(),
            'btn_primary': _("Submit"),
            'btn_default': _("Close"),
        }
        context = {
            'mark_nav_href': get_mark_nav_href(pk, page_num, line_num),
            'action': 'post',
            'modal_form': modal_form,
        }
        return render(request, 'pdf/mark.html', context)
    
    elif request.method == 'POST':
        mark = Mark()
        mark.uid = request.user.id
        mark.username = request.user.username
        mark.pdf_id = pk
        mark.page_num = page_num
        mark.line_num = line_num
        mark.content = request.POST['content']
        mark.date_create = now()
        mark.save()
        
        pdf_instance = pdfModel.objects.get(pk=pk)
        pdf_instance.mark += 1
        pdf_instance.save()
        return HttpResponse('')
        #pass
        #return redirect("/pdf/mark_view/%s/%s/%s/" % (pk, page_num, line_num))

def mark_view_line(request, **kwargs):
    
    pdf = pdfModel.objects.get(pk=kwargs['pk'])
    marklist = Mark.objects.filter(pdf_id=kwargs['pk'],page_num=kwargs['page_num'],line_num=kwargs['line_num'],displayorder__gte=0).order_by("date_create")
       
    context = {
        'action': 'view',
        'view_type': 'line',
        'marklist': marklist,
        'mark_nav_href': get_mark_nav_href(kwargs['pk'], kwargs['page_num'], kwargs['line_num']),
        'pdf': pdf,
        'kwargs': kwargs,
    }
    
    return render(request, 'pdf/mark.html', context)
    

def mark_view_page(request, **kwargs):
    
    pdf = pdfModel.objects.get(pk=kwargs['pk'])
    marklist = Mark.objects.filter(pdf_id=kwargs['pk'],page_num=kwargs['page_num'],displayorder__gte=0).order_by("date_create")
    
    context = {
        'action': 'view',
        'view_type': 'page',
        'marklist': marklist,
        'mark_nav_href': get_mark_nav_href(kwargs['pk'], kwargs['page_num'], kwargs['line_num']),
        'pdf': pdf,
        'kwargs': kwargs,
    }
    
    return render(request, 'pdf/mark.html', context)
    
def mark_about(request,  **kwargs):
    
    context = {
        'action': 'about', 
        'mark_nav_href': get_mark_nav_href(kwargs['pk'], kwargs['page_num'], kwargs['line_num']),
    }
    return render(request, 'pdf/mark.html', context)

def mark_delete(request, pk):
    mark = Mark.objects.get(pk=pk)
    mark.delete()
    if not get_auth_author_admin(mark.uid, request.user.id, request.user.is_superuser):
        return showmessage(request, PERMISSION_ERROR)
    return HttpResponse('')


class PDFCommentView(FormView):
    template_name = "pdf/comment.html"
    form_class = PDFCommentForm
    
    action = 'new'
    comment_instance = None
    pdf_instance = None 
    
    def __init__(self, *args, **kwargs):
        self.breadcrumb = [HOME_BREAD] 
        super(PDFCommentView, self).__init__(*args, **kwargs)
        
    def get(self, *args, **kwargs):
        if not check_login(self.request):
            return redirect("/account/login/?next=%s" % self.request.get_full_path())
        if 'pk' in self.kwargs and self.kwargs['pk'].isdigit():
            self.action = 'edit'
            self.comment_instance = Comment.objects.get(pk=self.kwargs['pk'])
        
            if not get_auth_author_admin(self.comment_instance.uid, self.request.user.id, self.request.user.is_superuser):
                return showmessage(self.request, PERMISSION_ERROR)
        
        self.request.session.modified = True
        
        return super(PDFCommentView, self).get(*args, **kwargs)
    
    def get_initial(self):
        initial = super(PDFCommentView, self).get_initial()
        if self.action == 'edit':
            initial["title"] = self.comment_instance.title
            
        else:
            try:
                initial["title"] = self.request.session['custom_field_value']['title']
            except:
                pass
            
        return initial
    
    def get_context_data(self, **kwargs):
        context = super(PDFCommentView, self).get_context_data(**kwargs)
        if self.action == 'edit':
            context['head_title_text'] = _('Edit Comment')
            context['legend_text'] = _('Edit Comment')
            context['submit_btn_text'] = _('Submit')
            self.breadcrumb.append({'text': 'Edit Comment'})
        else:
            context['head_title_text'] = _('Create Comment')
            context['legend_text'] = _('Create Comment')
            context['submit_btn_text'] = _('Submit')
            self.breadcrumb.append({'text': 'Create Comment'})
            
        context['breadcrumb'] = self.breadcrumb
        initial_form_session_for_custom_field(context['form'], self.request.session)
        
        return context
    
    def post(self, *args, **kwargs):
        if not check_login(self.request):
            return redirect("/account/login/?next=%s" % self.request.get_full_path())
        if 'pk' in self.kwargs and self.kwargs['pk'].isdigit():
            self.action = 'edit'
            self.comment_instance = Comment.objects.get(pk=self.kwargs['pk'])
            
            if not get_auth_author_admin(self.comment_instance.uid, self.request.user.id, self.request.user.is_superuser):
                return showmessage(self.request, PERMISSION_ERROR)
        
        self.pdf_instance = pdfModel.objects.get(pk=self.kwargs['pdf_id'])
        
        return super(PDFCommentView, self).post(*args, **kwargs)
    
    def get_form(self, form_class):
        instance = form_class(**self.get_form_kwargs())
        if self.action == 'edit':
            pass
            #instance.fields.pop('store_file')
        return instance
    
    
    
    def form_valid(self, form):
        self.User = self.request.user
        save_cleaned_data(form.cleaned_data, self.request.session)
        #validate content
        content_validator= CharValidator(validate_key='content',
                                    validate_label='comment content',
                                    session=self.request.session, 
                                    post=self.request.POST,
                                    minlength=100)
        content_validate_result = content_validator.check()
        #validate rate_score
        rate_score_validator = IntegerValidator(validate_key='rate_score',
                                    validate_label='comment rate', 
                                    session=self.request.session, 
                                    post=self.request.POST)
        rate_score_validate_result = rate_score_validator.check()
        #validate success
        if content_validate_result and rate_score_validate_result:
            cleaned_content = content_validator.get_value()
            cleaned_rate_score = rate_score_validator.get_value()
            clear_form_session(self.request.session)
        #validate failed
        else:
            self.request.session.modified = True
            return redirect(self.request.get_full_path())
        
        
        
        
        if self.action == 'new':
            #save comment
            self.comment_save(form, commit=True, cleaned_content=cleaned_content, cleaned_rate_score=cleaned_rate_score, pdf=self.pdf_instance)
            #update comment count
            self.pdf_instance.comment += 1
            self.pdf_instance.save()
            message_body = _('Comment has been posted successfully')
        else:
            #update comment
            self.comment_update(form, commit=True, cleaned_content=cleaned_content, cleaned_rate_score=cleaned_rate_score)
            message_body = _('Comment has been successfully modified')
        
        messages.success(self.request, message_body)
        if 'next' in self.request.GET and self.request.GET['next']:
            return redirect(self.request.GET['next']);
        else:    
            return redirect('/pdf/view/%s/' % self.pdf_instance.id);
        
    def comment_save(self, form, commit=True, **kwargs):
        comment = Comment()
        comment.pdf_id = kwargs['pdf'].id
        comment.uid = self.User.id
        comment.username = self.User.username
        comment.title = form.cleaned_data.get('title')
        comment.content = kwargs['cleaned_content']
        comment.rate_score = kwargs['cleaned_rate_score']
        comment.date_create = now()
        
        if commit:
            comment.save()

    def comment_update(self, form, commit=True, **kwargs):
        comment = self.comment_instance
        comment.title = form.cleaned_data.get('title')
        comment.content = kwargs['content']
        comment.rate_score = kwargs['rate_score']
        if commit:
            comment.save()
