from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _
from article.models import ArticleIndex


class ArticlePostForm(forms.Form):
    
    
    title = forms.CharField(
        label=_("Title"),
        min_length=2,
        max_length=100,
        widget=forms.TextInput(),
        required=True,
    )
    
    displayorder = forms.CharField(
        label=_("Display order"),
        min_length=1,
        max_length=3,
        widget=forms.TextInput(),
        required=True,
        initial = '0',
    )
        
    def clean_displayorder(self):
        if not self.cleaned_data['displayorder'].isdigit():
            raise forms.ValidationError(_("Digit only for displayorder"))
        return self.cleaned_data['displayorder']
        
class ArticleIndexPostForm(forms.Form):
    
    
    title = forms.CharField(
        label=_("Title"),
        min_length=2,
        max_length=100,
        widget=forms.TextInput(),
        required=True,
    )
    
    description = forms.CharField(
        label=_("Description"),
        min_length=2,
        max_length=255,
        widget=forms.Textarea(),
    )
    
    
    displayorder = forms.CharField(
        label=_("Display order"),
        min_length=1,
        max_length=3,
        widget=forms.TextInput(),
        required=True,
        initial = '0',
    )
        
    def clean_displayorder(self):
        if not self.cleaned_data['displayorder'].isdigit():
            raise forms.ValidationError(_("Digit only for displayorder"))
        return self.cleaned_data['displayorder']
        