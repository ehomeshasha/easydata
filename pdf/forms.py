from __future__ import unicode_literals

from easydata.constant import CONTENT_TYPE
from django import forms
from django.utils.translation import ugettext_lazy as _


class PDFUploadForm(forms.Form):
    
    title = forms.CharField(
        label=_("Title"),
        min_length=2,
        max_length=100,
        widget=forms.TextInput(),
        required=True
    )
    
    description = forms.CharField(
        label=_("Description"),
        widget=forms.Textarea(),
        required=True
    )
    store_file = forms.FileField(
        label=_("PDF file"),
        widget=forms.FileInput(),
        required=True
    )
    
    def clean_store_file(self):
        store_file = self.cleaned_data.get('store_file')
        if store_file._size > 150*1024*1024:
            raise forms.ValidationError(_("file too large ( > 150mb )"))
        if store_file.content_type != CONTENT_TYPE['pdf']:
            raise forms.ValidationError(_("invalid file type, must be pdf"))
        end_pos = store_file._name.rfind(".")
        ext = store_file._name[end_pos+1:]
        if ext != 'pdf':
            raise forms.ValidationError(_("invalid file suffix, must be .pdf"))


class PDFCommentForm(forms.Form):
    
    title = forms.CharField(
        label=_("Title"),
        min_length=2,
        max_length=100,
        widget=forms.TextInput(),
        required=True
    )
    
    
    
    