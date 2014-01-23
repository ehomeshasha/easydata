from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _


class CodePostForm(forms.Form):
    
    code = forms.CharField(
        label=_("Code"),
        widget=forms.Textarea(),
        required=True,
    )
    
    title = forms.CharField(
        label=_("Title"),
        min_length=2,
        max_length=100,
        widget=forms.TextInput(),
        required=True,
    )
    
    description = forms.CharField(
        label=_("Description"),
        max_length=255,
        widget=forms.Textarea(),
        required=False,
    )
    
    brush = forms.ChoiceField(
        label=_("Language"),
        choices=(
            ('plain',_('Plain Text')),
            ('as3','ActionScript3'),
            ('bash','Bash/shell'),
            ('cf','ColdFusion'),
            ('csharp','C#'),
            ('cpp','C++'),
            ('css','CSS'),
            ('delphi','Delphi/Pascal'),
            ('diff','Diff'),
            ('erl','Erlang'),
            ('groovy','Groovy'),
            ('js','JavaScript'),
            ('java','Java'),
            ('jfx','JavaFX'),
            ('perl','Perl'),
            ('php','PHP'),
            ('ps','PowerShell'),
            ('py','Python'),
            ('rails','Ruby'),
            ('scala','Scala'),
            ('sql','SQL'),
            ('vb','Visual Basic'),
            ('xml','HTML/XML'),
        ),
        widget=forms.Select(),
        required=True,
        initial='plain',
    )
    
    gutter = forms.ChoiceField(
        label=_("Gutter"),
        choices=((0,'hide'),(1,'show'),),
        widget=forms.Select(),
        required=True,
        initial=1,
    )
    
    first_line = forms.IntegerField(
        label=_("First line on the gutter"),
        min_value=1,
        max_value=99999,
        widget=forms.TextInput(),
        required=True,
        initial=1,
    )
    
    collapse = forms.ChoiceField(
        label=_("Enable collapse"),
        choices=((0,'no'),(1,'yes'),),
        widget=forms.Select(),
        required=True,
        initial=0,
    )
    
    highlight = forms.CharField(
        label=_("Define highlight lines, seperate by comma"),
        max_length=255,
        widget=forms.TextInput(),
        required=False,
    )
    
    url_clickable = forms.ChoiceField(
        label=_("URL clickable"),
        choices=((0,'no'),(1,'yes'),),
        widget=forms.Select(),
        required=True,
        initial=0,
    )
    
    max_height = forms.ChoiceField(
        label=_("Set max height value(unit: px) here, left 0 to ignore this setting"),
        choices=(
            ('no_max_height','No max height'),
            ('max_height100',100),
            ('max_height150',150),
            ('max_height200',200),
            ('max_height250',250),
            ('max_height300',300),
            ('max_height500',500),
        ),
        widget=forms.Select(),
        initial='',
    )
    
    def clean_highlight(self):
        return ','.join([x for x in self.cleaned_data['highlight'].replace(" ","").split(",") if x.isdigit()])
        
        
    
