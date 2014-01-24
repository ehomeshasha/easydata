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
from django.utils.timezone import now
from article.forms import ArticlePostForm
from article.models import Article, ArticleIndex
from django import forms
from django.views.generic.detail import DetailView
from django.template import Template
from django.template import Context
from django.conf import settings
import re
#class ArticlePostView(FormView):
#    pass
def get_articleindex_choices(articleindex):
    l = []
    for index in articleindex:
        l.append((index.id, index.title))
    return tuple(l)
        

class ArticlePostView(FormView):
    template_name = "article/post.html"
    form_class = ArticlePostForm
    
    action = 'new'
    article_instance = None 
    
    def __init__(self, *args, **kwargs):
        self.breadcrumb = [HOME_BREAD,{'text': 'Article','href': '/article/list/'},]
        super(ArticlePostView, self).__init__(*args, **kwargs)
        
    def get(self, *args, **kwargs):
        
        if not check_login(self.request):
            return redirect("/account/login/?next=%s" % self.request.get_full_path())
        if 'pk' in self.kwargs and self.kwargs['pk'].isdigit():
            self.action = 'edit'
            self.article_instance = Article.objects.get(pk=self.kwargs['pk'])
        
        
        
        return super(ArticlePostView, self).get(*args, **kwargs)
    
    def get_initial(self):
        initial = super(ArticlePostView, self).get_initial()
        if self.action == 'edit':
            initial["title"] = self.article_instance.title
            initial["fid"] = self.article_instance.fid
            initial["displayorder"] = self.article_instance.displayorder
            
        return initial
    
    def get_context_data(self, **kwargs):
        context = super(ArticlePostView, self).get_context_data(**kwargs)
        initial_form_session_for_custom_field(context['form'], self.request.session)
        if self.action == 'edit':
            context['head_title_text'] = _('Article Edit')
            context['legend_text'] = _('Article Edit')
            context['submit_btn_text'] = _('Submit')
            self.breadcrumb.append({'text': 'Edit'})
            context['form'].choice_html = get_choices_html(cid=self.article_instance.cate_id,ctype='pdf')
            if hasattr(context['form'], 'custom_field_value') and context['form'].custom_field_value:
                context['form'].custom_field_value.update({'content': self.article_instance.content})
            else:
                context['form'].custom_field_value = {'content': self.article_instance.content}
            
        else:
            context['head_title_text'] = _('Post Article')
            context['legend_text'] = _('Post Article')
            context['submit_btn_text'] = _('Submit')
            self.breadcrumb.append({'text': 'Post'})
            context['form'].choice_html = get_choices_html(cid=0,ctype='pdf')

        
        context['breadcrumb'] = self.breadcrumb
        
        
        return context
    
    def post(self, *args, **kwargs):
        if not check_login(self.request):
            return redirect("/account/login/?next=%s" % self.request.get_full_path())
        if 'pk' in self.kwargs and self.kwargs['pk'].isdigit():
            self.action = 'edit'
            self.article_instance = Article.objects.get(pk=self.kwargs['pk'])
            
        return super(ArticlePostView, self).post(*args, **kwargs)
    
    def get_form(self, form_class):
        instance = form_class(**self.get_form_kwargs())
        fid = forms.ChoiceField(
            label=_("ArticleIndex"),
            choices=get_articleindex_choices(ArticleIndex.objects.filter(uid=self.request.user.id, displayorder__gte=0)),
            widget=forms.Select(),
            required=True,
            initial='',
        )
        
        instance.fields['fid'] = fid
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
            #save information about article to database
            self.article_save(form, commit=True, cate_id=cleaned_cate_id, content=self.request.POST['content'])
            message_body = _('Article has been successfully posted')
        else:
            #update article information
            self.article_update(form, commit=True, cate_id=cleaned_cate_id, content=self.request.POST['content'])
            message_body = _('Information about this Article has been successfully modified')
        
        messages.success(self.request, message_body)
        return redirect('/article/list/');
        
    def article_save(self, form, commit=True, **kwargs):
        article = Article()
        article.title = form.cleaned_data.get("title")
        article.fid = form.cleaned_data.get("fid")
        article.cate_id = kwargs['cate_id']
        article.content = kwargs['content']
        article.displayorder = form.cleaned_data.get("displayorder")
        article.uid = self.User.id
        article.username = self.User.username
        article.date_create = now()
        article.date_update = now()
        
        if commit:
            article.save()

    def article_update(self, form, commit=True, **kwargs):
        article = self.article_instance
        article.title = form.cleaned_data.get("title")
        article.fid = form.cleaned_data.get("fid")
        article.cate_id = kwargs['cate_id']
        article.content = kwargs['content']
        article.displayorder = form.cleaned_data.get("displayorder")
        article.date_update = now()
        
        if commit:
            article.save()


class ArticleView(DetailView):
    
    model = Article
    template_name = "article/view.html"
    code_pattern = re.compile(r'(<p>){0,1}\s*({%\s*get_code\s*\d+\s*%})\s*(</p>){0,1}')
    s_pattern = re.compile(r'\s+')
    
    def __init__(self, *args, **kwargs):
        self.breadcrumb = [HOME_BREAD,{'text': 'Article','href': '/article/list/'},]
        super(ArticleView, self).__init__(*args, **kwargs)
    
    def get(self, *args, **kwargs):
        return super(ArticleView, self).get(*args, **kwargs)    
    
    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        article_instance = context['article']
        context['head_title_text'] = article_instance.title
        self.breadcrumb.append({'text': article_instance.title})
        context['breadcrumb'] = self.breadcrumb
        context['SITE_URL'] = settings.SITE_URL
        context['content'] = re.sub(self.code_pattern, self.render_code, article_instance.content)
        return context
    
    def render_code(self, m):
        code_syntax_string = re.sub(self.s_pattern, " ", m.group(2))
        t = Template("%s%s" % ("{% load custom_tags %}", code_syntax_string))
        return t.render(Context({}))