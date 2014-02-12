from __future__ import unicode_literals

from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import FormView

from django.http.response import HttpResponse

from easydata.func.function_core import check_login, get_add_icon
from django.contrib import messages
from easydata.constant import HOME_BREAD, PERPAGE
from django.utils.timezone import now
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from note.forms import NotePostForm
from note.models import Note



class NotePostView(FormView):
    template_name = "note/post.html"
    form_class = NotePostForm
    
    action = 'new'
    note_instance = None 
    
    def __init__(self, *args, **kwargs):
        self.breadcrumb = [HOME_BREAD,{'text': _('Note'),'href': '/note/list/'},]
        super(NotePostView, self).__init__(*args, **kwargs)
        
    def get(self, *args, **kwargs):
        
        if not check_login(self.request):
            return redirect("/account/login/?next=%s" % self.request.get_full_path())
        if 'pk' in self.kwargs and self.kwargs['pk'].isdigit():
            self.action = 'edit'
            self.note_instance = Note.objects.get(pk=self.kwargs['pk'])
        
        
        
        return super(NotePostView, self).get(*args, **kwargs)
    
    def get_initial(self):
        initial = super(NotePostView, self).get_initial()
        if self.action == 'edit':
            initial["content"] = self.note_instance.content
            
        return initial
    
    def get_context_data(self, **kwargs):
        context = super(NotePostView, self).get_context_data(**kwargs)
        if self.action == 'edit':
            context['head_title_text'] = _('Note Edit')
            context['legend_text'] = _('Note Edit')
            context['submit_btn_text'] = _('Submit')
            self.breadcrumb.append({'text': 'Edit'})
            
        else:
            context['head_title_text'] = _('Post Note')
            context['legend_text'] = _('Post Note')
            context['submit_btn_text'] = _('Submit')
            self.breadcrumb.append({'text': 'Post'})
        
        context['breadcrumb'] = self.breadcrumb
        
        return context
    
    def post(self, *args, **kwargs):
        if not check_login(self.request):
            return redirect("/account/login/?next=%s" % self.request.get_full_path())
        if 'pk' in self.kwargs and self.kwargs['pk'].isdigit():
            self.action = 'edit'
            self.note_instance = Note.objects.get(pk=self.kwargs['pk'])
            
        return super(NotePostView, self).post(*args, **kwargs)
    
    def form_valid(self, form):
        
        self.User = self.request.user
        
        if self.action == 'new':
            #save note
            self.note_save(form, commit=True)
            message_body = _('Note has been successfully posted')
        else:
            #update note
            self.note_update(form, commit=True)
            message_body = _('Note has been successfully modified')
        
        messages.success(self.request, message_body)
        return redirect('/note/list/');
        
    def note_save(self, form, commit=True):
        note = Note()
        note.content = form.cleaned_data.get("content")
        note.uid = self.User.id
        note.username = self.User.username
        note.date_create = now()
        note.date_update = now()
        
        if commit:
            note.save()

    def note_update(self, form, commit=True):
        note = self.note_instance
        note.content = form.cleaned_data.get("content")
        note.date_update = now()
        
        if commit:
            note.save()


class NoteView(DetailView):
    
    model = Note
    template_name = "note/view.html"
    
    def __init__(self, *args, **kwargs):
        self.breadcrumb = [HOME_BREAD,{'text': _('Note'),'href': '/note/list/'},]
        super(NoteView, self).__init__(*args, **kwargs)
    
    def get(self, *args, **kwargs):
        return super(NoteView, self).get(*args, **kwargs)    
    
    def get_context_data(self, **kwargs):
        context = super(NoteView, self).get_context_data(**kwargs)
        context['head_title_text'] = _('Note View')
        self.breadcrumb.append({'text': _('View')})
        context['breadcrumb'] = self.breadcrumb
        return context
    
class NoteListView(ListView):
    
    model = Note
    template_name = "note/list.html"
    paginate_by = PERPAGE
    
    def __init__(self, *args, **kwargs):
        self.breadcrumb = [HOME_BREAD,{'text': _('Note')},get_add_icon('/note/new/',_('Create new note'))] 
        super(NoteListView, self).__init__(*args, **kwargs)
    
    def get(self, *args, **kwargs):
        if not check_login(self.request):
            return redirect("/account/login/?next=%s" % self.request.get_full_path())
        return super(NoteListView, self).get(*args, **kwargs)
        
    def get_queryset(self):
        return Note.objects.filter(uid=self.request.user.id,displayorder__gte=0).order_by("-date_create")
    
    def get_context_data(self, **kwargs):
        context = super(NoteListView, self).get_context_data(**kwargs)
        context['head_title_text'] = _('Note List')
        context['breadcrumb'] = self.breadcrumb
        
        return context 


def delete_note(request, pk):
    note = Note.objects.get(pk=pk)
    note.delete()
    message_body = _("This note has been deleted")  
    messages.success(request, message_body)
    return HttpResponse('')





