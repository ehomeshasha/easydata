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
        html = '<a href="javascript:;" title="%s" class="code_title text-danger" data-id="%d">%s</a>\
                <pre class="%s">%s</pre>' % (
                    self.code.description, 
                    self.code.id,
                    self.code.title, 
                    self.get_class_configuration(), 
                    self.code.code,
                ) 
        return html
        