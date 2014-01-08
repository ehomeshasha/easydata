def initial_form_session_for_custom_field(form, session):
    if 'custom_field_error_css' in session and session['custom_field_error_css']:
        form.custom_field_error_css = session['custom_field_error_css']
    else:
        form.custom_field_error_css = None
        
    if 'custom_field_error_text' in session and session['custom_field_error_text']:
        form.custom_field_error_text = session['custom_field_error_text']
    else:
        form.custom_field_error_text = None

def clear_form_session_for_custom_field(session):
    session['custom_field_error_css'] = None
    session['custom_field_error_text'] = None
    
def set_form_session_for_custom_field(css, text, session):
    session['custom_field_error_css'] = css
    session['custom_field_error_text'] = text