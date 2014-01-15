from easydata.func.function_session import set_form_session_for_custom_field,\
    clear_form_session_for_custom_field, save_value_session_for_custom_field
from django.utils.translation import ugettext as _

def save_cleaned_data(cleaned_data, session):
    for key,value in cleaned_data.items():
        save_value_session_for_custom_field(key=key, value=value, session=session)


class Validator():
    
    value = None
    
    def __init__(self, validate_key, session, post, validate_label=None):
        self.validate_key = validate_key
        self.session = session
        self.post = post
        if validate_label:
            self.validate_label = validate_label
        else:
            self.validate_label = validate_key
        self.save_value()
        
    def check(self):
        if self.validate_key not in self.post or not self.post[self.validate_key]:
            self.error_text = [_("%s cannot be empty" % self.validate_label)]
            self.do_invalid()
            return False
        
        self.validate_value = self.post[self.validate_key]
        self.do_valid()
        return True
        
    def get_value(self):
        return self.validate_value    
    
    def get_key(self):
        return self.validate_key
    
    def do_valid(self):
        clear_form_session_for_custom_field(self.validate_key, self.session)
        
    def do_invalid(self, css='has-error'):
        set_form_session_for_custom_field(key=self.validate_key, text=self.error_text, session=self.session)
    
    def save_value(self):
        try:
            self.value = self.post[self.validate_key]
            save_value_session_for_custom_field(key=self.validate_key, value=self.value, session=self.session)
        except KeyError:
            self.value = None
            save_value_session_for_custom_field(key=self.validate_key, value=self.value, session=self.session)
    
class CharValidator(Validator):
    
    def __init__(self, validate_key, session, post, minlength=None, maxlength=None, validate_label=None):
        self.validate_key = validate_key
        self.session = session
        self.post = post
        self.minlength = minlength
        self.maxlength = maxlength
        if validate_label:
            self.validate_label = validate_label
        else:
            self.validate_label = validate_key
        self.save_value()
    
    def check(self):
        if self.validate_key not in self.post or not self.post[self.validate_key]:
            self.error_text = [_("%s cannot be empty" % self.validate_label)]
            self.do_invalid()
            return False
        
        if self.minlength and isinstance(self.minlength, int) and \
            len(self.post[self.validate_key]) < self.minlength:
            self.error_text = [_("%s must longer than %d characters" % (self.validate_label, self.minlength))]
            self.do_invalid()
            return False
    
        if self.maxlength and isinstance(self.maxlength, int) and \
            len(self.post[self.validate_key]) > self.maxlength:
            self.error_text = [_("%s exceed %d characters" % (self.validate_label, self.minlength))]
            self.do_invalid()
            return False
        self.validate_value = self.post[self.validate_key]
        self.do_valid()
        return True
  
        
class IntegerValidator(Validator):
    
    
        
    def check(self):
        if self.validate_key not in self.post or not self.post[self.validate_key]:
            self.error_text = [_("%s cannot be empty" % self.validate_label)]
            self.do_invalid()
            return False
        
        if not self.post[self.validate_key].isdigit():
            self.error_text = [_("%s is not digit" % self.validate_label)]
            self.do_invalid()
            return False
            
        self.validate_value = self.post[self.validate_key]
        self.do_valid()
        return True