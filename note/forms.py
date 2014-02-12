from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _


class NotePostForm(forms.Form):
    
    
    content = forms.CharField(
        label=_("Content"),
        min_length=2,
        widget=forms.Textarea(),
        required=True,
    )
    
        