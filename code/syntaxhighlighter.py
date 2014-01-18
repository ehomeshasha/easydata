from code.models import Mark
from django.utils.html import strip_tags
class Syntaxhighlighter():
    
    def __init__(self, code):
        self.code = code
        
    def get_class_configuration(self):
        class_text = 'brush: %s;toolbar: true;' % self.code.brush
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
        html = '<div style="margin-right:30px;">\
                    <a href="javascript:;" title="%s" class="code_title text-danger" data-id="%d">%s</a>\
                    <pre class="%s">%s</pre></div>' % (
                    self.code.description, 
                    self.code.id,
                    self.code.title, 
                    self.get_class_configuration(), 
                    self.code.code,
                ) 
        return html
        
        
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
                mark_html += '<div code_id="%d" line_num="%d" class="mark_wrapper"><a code_id="%d" line_num="%d" href="javascript:;" class="single_mark mark_view">%s</a></div>' \
                % (self.code.id, k, self.code.id, k, strip_tags(v[0].content))
            else:
                mark_html += '<div code_id="%d" line_num="%d" class="mark_wrapper"><a code_id="%d" line_num="%d" href="javascript:;" class="multi_mark mark_view">%d</a></div>' \
                % (self.code.id, k, self.code.id, k, len(v))
        
        
        return mark_html