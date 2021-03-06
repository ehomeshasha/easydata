from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

class CategoryPostForm(forms.Form):
    
    name = forms.CharField(
        label=_("Name"),
        min_length=2,
        max_length=30,
        widget=forms.TextInput(),
        required=True,
    )
    
    description = forms.CharField(
        label=_("Description"),
        max_length=255,
        widget=forms.Textarea(),
        required=False,
    )
    
    ctype = forms.ChoiceField(
        label=_("Module"),
        choices=(('learning','Learning'),('pdf','PDF'),('tiku', 'Tiku')),
        widget=forms.Select(),
        required=True,
        initial='learning',
    )
    
    displayorder = forms.IntegerField(
        label=_("Display Order"),
        max_value = 99999,
        widget=forms.TextInput(),
        required=True,
        initial=0,
    )
    
    status = forms.ChoiceField(
        label=_("Whether display"),
        choices=((0,'no'),(1,'yes'),),
        widget=forms.Select(),
        required=True,
        initial=1,
    )
    
    #def clean_displayorder(self):
    #    if not self.cleaned_data['displayorder'].isdigit():
    #        raise forms.ValidationError(_("Digit only for displayorder"))
    #    return self.cleaned_data['displayorder']
        
        
