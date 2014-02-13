from __future__ import unicode_literals

from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import FormView

from django.http.response import HttpResponse

from django.views.generic.base import TemplateView
from easydata.category.models import category
from easydata.category.forms import CategoryPostForm
from easydata.func.function_session import initial_form_session_for_custom_field,\
    clear_form_session
from easydata.func.function_category import get_category_fid_choices_html,\
    get_category_list_html
from easydata.func.function_core import check_login, get_add_icon
from django.contrib import messages
from easydata.constant import HOME_BREAD
from easydata.validator import IntegerValidator


class CategoryPostView(FormView):
    template_name = 'category/post.html'
    form_class = CategoryPostForm
    action = 'new'
    category_instance = None 
    custom_field_css = None
    custom_field_errors = []
    
    def __init__(self, *args, **kwargs):
        self.breadcrumb = [HOME_BREAD,{'text': _('Category'), 'href': '/category/list/'},] 
        super(CategoryPostView, self).__init__(*args, **kwargs)
    
    def get(self, *args, **kwargs):
        if not check_login(self.request) or self.request.user.is_superuser != True:
            return redirect("/account/login/?next=%s" % self.request.get_full_path())
        if 'pk' in self.kwargs and self.kwargs['pk'].isdigit():
            self.action = 'edit'
            self.category_instance = category.objects.get(pk=self.kwargs['pk'])
        
        
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
            context['legend_text'] = _('Category Edit')
            self.breadcrumb.append({'text': 'Edit'})
        else:
            context['head_title_text'] = _('New Category')
            context['legend_text'] = _('New Category')
            self.breadcrumb.append({'text': 'Create'})
        
        context['breadcrumb'] = self.breadcrumb
        initial_form_session_for_custom_field(context['form'], self.request.session)
        
        return context
    
    def post(self, *args, **kwargs):
        if not check_login(self.request) or self.request.user.is_superuser != True:
            return redirect("/account/login/?next=%s" % self.request.get_full_path())
        if 'pk' in self.kwargs and self.kwargs['pk'].isdigit():
            self.action = 'edit'
            self.category_instance = category.objects.get(pk=self.kwargs['pk'])
        return super(CategoryPostView, self).post(*args, **kwargs)
    
    def form_valid(self, form):
        if not check_login(self.request) or self.request.user.is_superuser != True:
            return redirect("/account/login/")
        else:
            
            #validate fid
            fid_validator = IntegerValidator(validate_key='fid',
                                        validate_label='father category id', 
                                        session=self.request.session, 
                                        post=self.request.POST)
            fid_validate_result = fid_validator.check()
            if fid_validate_result:
                cleaned_fid = fid_validator.get_value()
                clear_form_session(self.request.session)
            else:
                self.request.session.modified = True
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
                message_body = _('category is successfully created')
            else:
                self.category_instance.fid = cleaned_fid
                self.category_instance.name = form.cleaned_data.get("name")
                self.category_instance.description = form.cleaned_data.get("description")
                self.category_instance.status = form.cleaned_data.get("status")
                self.category_instance.displayorder = form.cleaned_data.get("displayorder")
                self.category_instance.ctype = form.cleaned_data.get("ctype")
                self.category_instance.save()
                message_body = _('category has been successfully modified')
                
            messages.success(self.request, message_body)
            
            return redirect('/category/list/')
            

class CategoryListView(TemplateView):
    model = category
    template_name = 'category/list.html'
    
    def __init__(self, *args, **kwargs):
        self.breadcrumb = [HOME_BREAD,{'text': _('Category')},get_add_icon('/category/new/',_('Create a new category'))] 
        super(CategoryListView, self).__init__(*args, **kwargs)
    
    def get(self, *args, **kwargs):
        if not check_login(self.request) or self.request.user.is_superuser != True:
            return redirect("/account/login/?next=%s" % self.request.get_full_path())
        return super(CategoryListView, self).get(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['category_list_html'] = get_category_list_html()
        context['head_title_text'] = _('Category List') 
        context['breadcrumb'] = self.breadcrumb
        return context
    
def delete_category(request, pk):
    cate = category.objects.get(pk=pk)
    if not check_login(request) or request.user.is_superuser != True:
        return redirect("/account/login/?next=%s" % request.get_full_path())
    cate.delete()
    message_body = "The category %s has been deleted" % cate.name  
    messages.success(request, message_body)
    return HttpResponse('')


