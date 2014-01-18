from __future__ import unicode_literals

from django.shortcuts import redirect, render
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import FormView

from django.http.response import HttpResponse

from django.views.generic.base import TemplateView
from easydata.category.models import category
from easydata.category.forms import CategoryPostForm
from easydata.func.function_session import initial_form_session_for_custom_field,\
    clear_form_session
from easydata.func.function_category import get_category_fid_choices_html,\
    get_category_list_html, get_choices_html
from easydata.func.function_core import check_login
from django.contrib import messages
from easydata.constant import HOME_BREAD
from easydata.validator import IntegerValidator
from code.models import Code, Mark
from code.forms import CodePostForm
from django.utils.timezone import now
#class CodePostView(FormView):
#    pass


class CodePostView(FormView):
    template_name = "code/post.html"
    form_class = CodePostForm
    
    action = 'new'
    code_instance = None 
    
    def __init__(self, *args, **kwargs):
        self.breadcrumb = [HOME_BREAD,{'text': 'Code','href': '/code/list/'},] 
        super(CodePostView, self).__init__(*args, **kwargs)
        
    def get(self, *args, **kwargs):
        
        if not check_login(self.request):
            return redirect("/account/login/?next=%s" % self.request.get_full_path())
        if 'pk' in self.kwargs and self.kwargs['pk'].isdigit():
            self.action = 'edit'
            self.code_instance = Code.objects.get(pk=self.kwargs['pk'])
        
        
        
        return super(CodePostView, self).get(*args, **kwargs)
    
    def get_initial(self):
        initial = super(CodePostView, self).get_initial()
        if self.action == 'edit':
            initial["code"] = self.code_instance.code
            initial["title"] = self.code_instance.title
            initial["description"] = self.code_instance.description
            initial["brush"] = self.code_instance.brush
            initial["gutter"] = self.code_instance.gutter
            initial["first_line"] = self.code_instance.first_line
            initial["collapse"] = self.code_instance.collapse
            initial["highlight"] = self.code_instance.highlight
            initial["url_clickable"] = self.code_instance.url_clickable
            
        return initial
    
    def get_context_data(self, **kwargs):
        context = super(CodePostView, self).get_context_data(**kwargs)
        if self.action == 'edit':
            context['head_title_text'] = _('Code Edit')
            context['legend_text'] = _('Code Edit')
            context['submit_btn_text'] = _('Submit')
            self.breadcrumb.append({'text': 'Edit'})
            context['form'].choice_html = get_choices_html(cid=self.code_instance.cate_id,ctype='pdf')
        else:
            context['head_title_text'] = _('Post Code')
            context['legend_text'] = _('Post Code')
            context['submit_btn_text'] = _('Submit')
            self.breadcrumb.append({'text': 'Post'})
            context['form'].choice_html = get_choices_html(cid=0,ctype='pdf')
        
        context['breadcrumb'] = self.breadcrumb
        initial_form_session_for_custom_field(context['form'], self.request.session)
        
        return context
    
    def post(self, *args, **kwargs):
        if not check_login(self.request):
            return redirect("/account/login/?next=%s" % self.request.get_full_path())
        if 'pk' in self.kwargs and self.kwargs['pk'].isdigit():
            self.action = 'edit'
            self.code_instance = Code.objects.get(pk=self.kwargs['pk'])
            
        return super(CodePostView, self).post(*args, **kwargs)
    
    def get_form(self, form_class):
        instance = form_class(**self.get_form_kwargs())
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
            #save information about code to database
            self.code_save(form, commit=True, cate_id=cleaned_cate_id)
            message_body = _('Code has been successfully posted')
        else:
            #update code information
            self.code_update(form, commit=True, cate_id=cleaned_cate_id)
            message_body = _('Information about this Code has been successfully modified')
        
        messages.success(self.request, message_body)
        return redirect('/code/list/');
        
    def code_save(self, form, commit=True, **kwargs):
        code = Code()
        code.code = form.cleaned_data.get("code")
        code.title = form.cleaned_data.get("title")
        code.cate_id = kwargs['cate_id']
        code.description = form.cleaned_data.get("description")
        code.uid = self.User.id
        code.username = self.User.username
        
        code.brush = form.cleaned_data.get("brush")
        code.gutter = form.cleaned_data.get("gutter")
        code.first_line = form.cleaned_data.get("first_line")
        code.collapse = form.cleaned_data.get("collapse")
        code.highlight = form.cleaned_data.get("highlight")
        code.url_clickable = form.cleaned_data.get("url_clickable")
        
        code.date_create = now()
        code.date_update = now()
        
        if commit:
            code.save()

    def code_update(self, form, commit=True, **kwargs):
        code = self.code_instance
        code.code = form.cleaned_data.get("code")
        code.title = form.cleaned_data.get("title")
        code.cate_id = kwargs['cate_id']
        code.description = form.cleaned_data.get("description")
        
        code.brush = form.cleaned_data.get("brush")
        code.gutter = form.cleaned_data.get("gutter")
        code.first_line = form.cleaned_data.get("first_line")
        code.collapse = form.cleaned_data.get("collapse")
        code.highlight = form.cleaned_data.get("highlight")
        code.url_clickable = form.cleaned_data.get("url_clickable")
        
        code.date_update = now()
        if commit:
            code.save()


def get_mark_nav_href(pk, line_num):
    return {
        'post': '/code/mark_post/%s/%s/' % (pk, line_num),
        'view_line': '/code/mark_view_line/%s/%s/' % (pk, line_num),
        'about': '/code/mark_about/%s/%s/' % (pk, line_num),
    }

def mark_post(request, pk, line_num):
    
    if request.method == 'GET':
        modal_form = {
            'action': request.get_full_path(),
            'btn_primary': _("Submit"),
            'btn_default': _("Close"),
        }
        context = {
            'mark_nav_href': get_mark_nav_href(pk, line_num),
            'action': 'post',
            'modal_form': modal_form,
        }
        return render(request, 'code/mark.html', context)
    
    elif request.method == 'POST':
        mark = Mark()
        mark.uid = request.user.id
        mark.username = request.user.username
        mark.code_id = pk
        mark.line_num = line_num
        mark.content = request.POST['content']
        mark.date_create = now()
        mark.save()
        
        code_instance = Code.objects.get(pk=pk)
        code_instance.mark += 1
        code_instance.save()
        return HttpResponse('')
        

def mark_view_line(request, **kwargs):
    
    code = Code.objects.get(pk=kwargs['pk'])
    marklist = Mark.objects.filter(code_id=kwargs['pk'],line_num=kwargs['line_num'],displayorder__gte=0).order_by("date_create")
       
    context = {
        'action': 'view',
        'view_type': 'line',
        'marklist': marklist,
        'mark_nav_href': get_mark_nav_href(kwargs['pk'], kwargs['line_num']),
        'code': code,
        'kwargs': kwargs,
    }
    
    return render(request, 'code/mark.html', context)
    

def mark_about(request,  **kwargs):
    
    context = {
        'action': 'about', 
        'mark_nav_href': get_mark_nav_href(kwargs['pk'], kwargs['line_num']),
    }
    return render(request, 'code/mark.html', context)

def mark_delete(request, pk):
    Mark.objects.get(pk=pk).delete()
    return HttpResponse('')