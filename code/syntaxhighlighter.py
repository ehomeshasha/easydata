from code.models import Mark
from django.utils.html import strip_tags
from django import template
from django.utils.translation import ugettext as _

class Syntaxhighlighter():
    
    def __init__(self, code):
        self.code = code
        #noescape_brushs = ['js','jscript','javascript','php','xml','xhtml','xslt','html','xhtml']
        #if not self.code.brush in noescape_brushs:
        if True:
            self.code.code = template.defaultfilters.force_escape(self.code.code)
    
        
    def get_class_configuration(self):
        class_text = 'brush: %s;toolbar: true;class-name: \'%s\'' % (self.code.brush, self.code.max_height)
        if self.code.gutter == 0:
            class_text += 'gutter: false;'
        elif self.code.gutter == 1:
            class_text += 'gutter: true;first-line: %d;' % self.code.first_line
        if self.code.collapse == 0:
            class_text += 'collapse: false;'
        elif self.code.gutter == 1:
            class_text += 'collapse: true;'
        if self.code.highlight:
            class_text += 'highlight: [%s];' % self.code.highlight
        if self.code.url_clickable == 0:
            class_text += 'auto-links: false;'
        elif self.code.url_clickable == 1:
            class_text += 'auto-links: true;'
        if self.code.brush == 'php':
            class_text += 'html-script: true;'
        else:
            class_text += 'html-script: false;'
        return class_text    
        
    def get_code(self):
        html = '<a href="/code/edit/%d/?redirect=1" title="%s" class="code_title text-danger xw1" data-id="%d">%s</a>\
                <div class="row">\
                    <div class="col-lg-10 code_body" code_id="%d">\
                        <div class="hidden hidden_mark_view">%s</div>\
                        <pre class="%s">%s</pre>\
                    </div>\
                    <div class="col-lg-2 code_info">\
                    \
                    </div>\
                </div>\
                %s\
                ' % (
                    self.code.id,
                    self.code.description, 
                    self.code.id,
                    self.code.title,
                    self.code.id,
                    self.get_mark(),
                    self.get_class_configuration(), 
                    self.code.code,
                    self.get_description(),
                )
        
        return html
        
    def get_description(self):
        if not self.code.description:
            return ''
        desc = '<div class="row">\
                    <div class="col-lg-10 no-padding-right">\
                        <pre><h4 class="no-margin-top xw1">%s</h4>%s</pre>\
                    </div>\
                </div>' % (_('Code details'), self.code.description)
        return desc
        
    def get_mark(self):
        marks = Mark.objects.filter(code_id=self.code.id, displayorder__gte=0).order_by("line_num")
        mark_dict = {}
        for mark in marks:
            if not mark.line_num in mark_dict.keys():
                mark_dict[mark.line_num] = [mark]
            else:
                mark_dict[mark.line_num].append(mark)
        
        mark_html = ''
        for k,v in mark_dict.items():
            if len(v) == 1 and len(strip_tags(v[0].content)) < 20:
                #mark_html += '<div code_id="%d" line_num="%d" class="mark_wrapper"><a code_id="%d" line_num="%d" href="javascript:;" class="single_mark mark_view" data-toggle="tooltip" data-placement="right" data-trigger="manual" data-title="%s">&nbsp;</a></div>' \
                mark_html += '<div code_id="%d" line_num="%d" class="mark_wrapper">\
                                <div class="tooltip fade right in" style="top: 0px; left: -2px; display: block;">\
                                    <div class="tooltip-arrow"></div>\
                                    <div class="tooltip-inner"><a code_id="%d" line_num="%d" href="javascript:;" class="single_mark mark_view" title="">%s</a></div>\
                                </div>\
                            </div>'\
                % (self.code.id, k, self.code.id, k, strip_tags(v[0].content))
            else:
                #mark_html += '<div code_id="%d" line_num="%d" class="mark_wrapper"><a code_id="%d" line_num="%d" href="javascript:;" class="multi_mark mark_view" data-toggle="tooltip" data-placement="right" data-trigger="manual" data-title="%d">&nbsp;</a></div>' \
                mark_html += '<div code_id="%d" line_num="%d" class="mark_wrapper">\
                                <div class="tooltip fade right in" style="top: 0px; left: -2px; display: block;">\
                                    <div class="tooltip-arrow"></div>\
                                    <div class="tooltip-inner"><a code_id="%d" line_num="%d" href="javascript:;" class="multi_mark mark_view" title=""><span class="xw1 text-danger">%d</span> marks</a></div>\
                                </div>\
                            </div>'\
                % (self.code.id, k, self.code.id, k, len(v))
        
        
        return mark_html