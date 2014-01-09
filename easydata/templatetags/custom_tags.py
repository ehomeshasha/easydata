from django import template
from django.utils.timezone import now
register = template.Library()
from django.utils.translation import ugettext as _
@register.filter()
def hdate(value):
    timedelta = now() - value

    days = int(timedelta.days)
    seconds = int(timedelta.seconds)
    if days < 1:
        if seconds>3600:
            return str(int(seconds/3600))+_(" hours ago");
        elif seconds>1800:
            return _("half hour ago");
        elif seconds>60:
            return str(int(seconds/60))+_(" minutes ago");
        elif seconds>0:
            return str(seconds)+_(" seconds ago");
        elif seconds==0:
            return 'just now'
    elif days == 1:
        return _("yesterday")
    elif days < 7:
        return str(days)+_(" days ago")
    else:
        return template.defaultfilters.date(value, "SHORT_DATE_FORMAT")


@register.filter()
def hsize(size):
    num = int(size)
    for x in ['bytes','KB','MB','GB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')


@register.assignment_tag
def get_auth_author_admin(authorid, uid, is_superuser):
    if uid and (is_superuser or authorid == id):
        return True
    return False
