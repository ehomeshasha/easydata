from __future__ import unicode_literals

from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import FormView

from django.http.response import HttpResponse

from easydata.func.function_session import initial_form_session_for_custom_field,\
    clear_form_session
from easydata.func.function_category import get_choices_html, get_category_dict_pk
from easydata.func.function_core import check_login, get_add_icon, \
    get_pagination_from_rawqueryset, showmessage
from django.contrib import messages
from easydata.constant import HOME_BREAD, PERPAGE, PERMISSION_ERROR
from easydata.validator import IntegerValidator
from django.utils.timezone import now
from article.forms import ArticlePostForm, ArticleIndexPostForm
from article.models import Article, ArticleIndex
from django import forms
from django.views.generic.detail import DetailView
from django.template import Template
from django.template import Context
from django.conf import settings
import re
from django.views.generic.list import ListView
from easydata.templatetags.custom_tags import get_auth_author_admin


def get_articleindex_choices(articleindex):
    l = [(0, _("None"))]
    for index in articleindex:
        l.append((index.id, index.title))
    return tuple(l)
        

class ArticlePostView(FormView):
    template_name = "article/post.html"
    form_class = ArticlePostForm
    
    action = 'new'
    article_instance = None 
    
    def __init__(self, *args, **kwargs):
        self.breadcrumb = [HOME_BREAD,{'text': _('Article'),'href': '/article/list/'},]
        super(ArticlePostView, self).__init__(*args, **kwargs)
        
    def get(self, *args, **kwargs):
        
        if not check_login(self.request):
            return redirect("/account/login/?next=%s" % self.request.get_full_path())
        if 'pk' in self.kwargs and self.kwargs['pk'].isdigit():
            self.action = 'edit'
            self.article_instance = Article.objects.get(pk=self.kwargs['pk'])
            
            if not get_auth_author_admin(self.article_instance.uid, self.request.user.id, self.request.user.is_superuser):
                return showmessage(self.request, PERMISSION_ERROR)
                
        
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
            
            if not get_auth_author_admin(self.article_instance.uid, self.request.user.id, self.request.user.is_superuser):
                return showmessage(self.request, PERMISSION_ERROR)
            
        return super(ArticlePostView, self).post(*args, **kwargs)
    
    def get_form(self, form_class):
        instance = form_class(**self.get_form_kwargs())
        fid = forms.ChoiceField(
            label=_("ArticleIndex <a href='/article/indexnew/' target='_blank'>create ArticleIndex</a>"),
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
        self.breadcrumb = [HOME_BREAD,{'text': _('Article'),'href': '/article/list/'},]
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
    
class ArticleListView(ListView):
    model = Article
    template_name = "article/list.html"
    perpage = PERPAGE
    
    def __init__(self, *args, **kwargs):
        self.breadcrumb = [HOME_BREAD,{'text': _('Article')},get_add_icon('/article/new/',_('Create a new Article'))] 
        super(ArticleListView, self).__init__(*args, **kwargs)
    
    def get_queryset(self):
        #return Article.objects.filter(displayorder__gte=0).order_by("date_create")
        rawqueryset = Article.objects.raw("SELECT a.*,b.title AS articleindex_title FROM \
            article_article AS a LEFT JOIN article_articleindex AS b ON a.fid=b.id \
            WHERE a.displayorder>=0 ORDER BY a.date_create DESC")
        return rawqueryset
    
    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context['head_title_text'] = _('Article List')
        context['breadcrumb'] = self.breadcrumb
        context['category_dict_pk'] = get_category_dict_pk()
        context['article_list'], context['page_obj'], context['is_paginated'] = get_pagination_from_rawqueryset(context, self.perpage)
        
        return context


def delete_article(request, pk):
    article = Article.objects.get(pk=pk)
    if not get_auth_author_admin(article.uid, request.user.id, request.user.is_superuser):
        return showmessage(request, PERMISSION_ERROR)
    article.delete()
    message_body = _("This article has been deleted")  
    messages.success(request, message_body)
    return HttpResponse('')



class ArticleIndexPostView(FormView):
    template_name = "article/indexpost.html"
    form_class = ArticleIndexPostForm
    
    action = 'new'
    articleindex_instance = None 
    
    def __init__(self, *args, **kwargs):
        self.breadcrumb = [HOME_BREAD,{'text': _('ArticleIndex'),'href': '/article/indexlist/'},]
        super(ArticleIndexPostView, self).__init__(*args, **kwargs)
        
    def get(self, *args, **kwargs):
        
        if not check_login(self.request):
            return redirect("/account/login/?next=%s" % self.request.get_full_path())
        if 'pk' in self.kwargs and self.kwargs['pk'].isdigit():
            self.action = 'edit'
            self.articleindex_instance = ArticleIndex.objects.get(pk=self.kwargs['pk'])
        
            if not get_auth_author_admin(self.articleindex_instance.uid, self.request.user.id, self.request.user.is_superuser):
                return showmessage(self.request, PERMISSION_ERROR)
        
        return super(ArticleIndexPostView, self).get(*args, **kwargs)
    
    def get_initial(self):
        initial = super(ArticleIndexPostView, self).get_initial()
        if self.action == 'edit':
            initial["title"] = self.articleindex_instance.title
            initial["description"] = self.articleindex_instance.description
            initial["displayorder"] = self.articleindex_instance.displayorder
            
        return initial
    
    def get_context_data(self, **kwargs):
        context = super(ArticleIndexPostView, self).get_context_data(**kwargs)
        initial_form_session_for_custom_field(context['form'], self.request.session)
        if self.action == 'edit':
            context['head_title_text'] = _('ArticleIndex Edit')
            context['legend_text'] = _('ArticleIndex Edit')
            context['submit_btn_text'] = _('Submit')
            self.breadcrumb.append({'text': 'Edit'})
            context['form'].choice_html = get_choices_html(cid=self.articleindex_instance.cate_id,ctype='pdf')
            
            
        else:
            context['head_title_text'] = _('Post ArticleIndex')
            context['legend_text'] = _('Post ArticleIndex')
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
            self.articleindex_instance = ArticleIndex.objects.get(pk=self.kwargs['pk'])
            
            if not get_auth_author_admin(self.articleindex_instance.uid, self.request.user.id, self.request.user.is_superuser):
                return showmessage(self.request, PERMISSION_ERROR)
            
        return super(ArticleIndexPostView, self).post(*args, **kwargs)
    
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
            #save information about article to database
            self.articleindex_save(form, commit=True, cate_id=cleaned_cate_id)
            message_body = _('ArticleIndex has been successfully posted')
        else:
            #update article information
            self.articleindex_update(form, commit=True, cate_id=cleaned_cate_id)
            message_body = _('Information about this ArticleIndex has been successfully modified')
        
        messages.success(self.request, message_body)
        return redirect('/article/indexlist/');
        
    def articleindex_save(self, form, commit=True, **kwargs):
        articleindex = ArticleIndex()
        articleindex.title = form.cleaned_data.get("title")
        articleindex.description = form.cleaned_data.get("description")
        articleindex.cate_id = kwargs['cate_id']
        articleindex.displayorder = form.cleaned_data.get("displayorder")
        articleindex.uid = self.User.id
        articleindex.username = self.User.username
        articleindex.date_create = now()
        articleindex.date_update = now()
        
        if commit:
            articleindex.save()

    def articleindex_update(self, form, commit=True, **kwargs):
        articleindex = self.articleindex_instance
        articleindex.title = form.cleaned_data.get("title")
        articleindex.description = form.cleaned_data.get("description")
        articleindex.cate_id = kwargs['cate_id']
        articleindex.displayorder = form.cleaned_data.get("displayorder")
        articleindex.date_update = now()
        
        if commit:
            articleindex.save()














class ArticleIndexListView(ListView):
    
    model = ArticleIndex
    template_name = "article/indexlist.html"
    paginate_by = PERPAGE
    
    def __init__(self, *args, **kwargs):
        self.breadcrumb = [HOME_BREAD,{'text': _('ArticleIndex')},get_add_icon('/article/indexnew/',_('Create new ArticleIndex'))] 
        super(ArticleIndexListView, self).__init__(*args, **kwargs)
    
    def get(self, *args, **kwargs):
        if not check_login(self.request):
            return redirect("/account/login/?next=%s" % self.request.get_full_path())
        return super(ArticleIndexListView, self).get(*args, **kwargs)
        
    def get_queryset(self):
        return ArticleIndex.objects.filter(uid=self.request.user.id,displayorder__gte=0).order_by("-date_create")
    
    def get_context_data(self, **kwargs):
        context = super(ArticleIndexListView, self).get_context_data(**kwargs)
        context['head_title_text'] = _('ArticleIndex List')
        context['breadcrumb'] = self.breadcrumb
        context['category_dict_pk'] = get_category_dict_pk()
        
        for i,articleindex in enumerate(context['articleindex_list']):
            context['articleindex_list'][i].articles = Article.objects.filter(fid=articleindex.id,displayorder__gte=0).order_by("displayorder")
        
        return context 
    
    
def delete_articleindex(request, pk):
    articleindex = ArticleIndex.objects.get(pk=pk)
    if not get_auth_author_admin(articleindex.uid, request.user.id, request.user.is_superuser):
        return showmessage(request, PERMISSION_ERROR)
    articleindex.delete()
    message_body = _("This articleindex has been deleted")  
    messages.success(request, message_body)
    return HttpResponse('')






