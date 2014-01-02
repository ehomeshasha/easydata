from django.db import models
import datetime
from django.utils import timezone
from easydata.db.mysql.fields import NormalTextField, C_IntegerField, C_SmallIntegerField
# Create your models here.
class Poll(models.Model):
    title = models.CharField(max_length=50)
    pub_date = models.DateTimeField('date published')
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.question
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)  # @UndefinedVariable
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
    
    
class Data(models.Model):
    
    uid = C_IntegerField(max_length=11, default=0)
    username = models.CharField(max_length=30)
    groupids = models.CharField(max_length=255)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    store_file = models.FileField(upload_to='data/upload')
    store_filepath = models.FilePathField(verbose_name='Store Path')
    tag = models.CharField(max_length=255)
    cate_id = C_SmallIntegerField(max_length=5, default=0)
    dateline = C_IntegerField(max_length=10, default=0)
    code = NormalTextField()
    def __unicode__(self):
        return self.title
    

    
    
'''    
username = models.CharField(_('username'), max_length=30, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                    '@/./+/-/_ characters'),
        validators=[
            validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'), 'invalid')
        ])
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
'''