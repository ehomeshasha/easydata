def initial_form_session_for_custom_field(form, session):
    if 'custom_field_error_css' in session and session['custom_field_error_css']:
        form.custom_field_error_css = session['custom_field_error_css']
    else:
        form.custom_field_error_css = None
        
    if 'custom_field_error_text' in session and session['custom_field_error_text']:
        form.custom_field_error_text = session['custom_field_error_text']
    else:
        form.custom_field_error_text = None
        
    if 'custom_field_value' in session and session['custom_field_value']:
        form.custom_field_value = session['custom_field_value']
    else:
        form.custom_field_value = None

def clear_form_session(session):
    session['custom_field_error_css'] = {}
    session['custom_field_error_text'] = {}
    session['custom_field_value'] = {}
    session.modified = True

def clear_form_session_for_custom_field(key, session):
    try:
        del(session['custom_field_error_css'][key])
        del(session['custom_field_error_text'][key])
    except:
        pass
    
def set_form_session_for_custom_field(key, text, session, css=u'has-error'):
    if 'custom_field_error_css' not in session or 'custom_field_error_text' not in session:
        session['custom_field_error_css'] = {}
        session['custom_field_error_text'] = {}
    session['custom_field_error_css'][key] = css
    session['custom_field_error_text'][key] = text

def save_value_session_for_custom_field(key, value, session):
    if 'custom_field_value' not in session:
        session['custom_field_value'] = {}
    session['custom_field_value'][key] = value