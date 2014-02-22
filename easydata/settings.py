import os

if not "/home/hadoop-user/workspace/easydata" in __file__:
    import uwsgi
    from uwsgidecorators import timer
    from django.utils import autoreload
    
    @timer(3)
    def change_code_gracefull_reload(sig):
        if autoreload.code_changed():
            uwsgi.reload()

SITE_URL = 'http://127.0.0.1:8000'

ALLOWED_HOSTS = []
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = [
    # ("Your Name", "your_email@example.com"),
]

MANAGERS = ADMINS

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        'NAME': 'easydata',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'root',
        'PASSWORD': 'zzy8945620',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
        'OPTIONS': {  
                    'init_command': 'SET storage_engine=MyISAM',  
        },
    }
}


#import _mysql

#mysql_host = 'localhost'
#mysql_user = 'root'
#mysql_passwd = 'zzy8945620'
#mysql_dbname = 'tianchai'
##mysql_host = '42.121.53.20'
#mysql_user = 'root'
#mysql_passwd = 'jz100OnlineJudge'
#mysql_dbname = 'tianchai'
#JZ100DB=_mysql.connect(host=mysql_host,user=mysql_user,passwd=mysql_passwd,db=mysql_dbname)

#import MySQLdb as mdb


#JZ_CON = mdb.connect(mysql_host, mysql_user, mysql_passwd, mysql_dbname);






# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "Asia/Shanghai"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "zh-cn"
ugettext = lambda s: s

LANGUAGES = (
    ('zh-cn', ugettext('Chinese')),
    ('en', ugettext('English')),
)
LOCALE_PATHS = (
    os.path.join(PROJECT_ROOT, "locale"),
    
)

SITE_ID = int(os.environ.get("SITE_ID", 1))

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT= os.path.join(PROJECT_ROOT,'media_files')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "/media_files/"

# Absolute path to the directory static files should be collected to.
# Don"t put anything in this directory yourself; store your static files
# in apps" "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PACKAGE_ROOT, "site_media", "static")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/static/"

# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(PACKAGE_ROOT, "static"),
    
]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Make this unique, and don't share it with anybody.
SECRET_KEY = "+i)fz)h2(57suvi$aztx#pv4w4!0-_cw*1_!)pl3ausm(qr#p("

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    "account.context_processors.account",
    "pinax_theme_bootstrap.context_processors.theme",
    "easydata.context_processors.constant",
]


MIDDLEWARE_CLASSES = [
    "easydata.middleware.ForceDefaultLanguageMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    
    #i18n
    'django.middleware.locale.LocaleMiddleware',
    'account.middleware.LocaleMiddleware',
    'account.middleware.TimezoneMiddleware',
    
]

ROOT_URLCONF = "easydata.urls"

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = "easydata.wsgi.application"

TEMPLATE_DIRS = [
    os.path.join(PACKAGE_ROOT, "templates"),
    os.path.join(PACKAGE_ROOT, "category/templates"),
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    
    # theme
    "bootstrapform",
    "pinax_theme_bootstrap",
    
    # external
    "account",
    "eventlog",
    "metron",
    
    # project
    "easydata",
    
    #myapps
    "pdf",
    "article",
    "code",
    "note",
]

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse"
        }
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler"
        }
    },
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
    }
}

FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, "fixtures"),
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_USE_OPENID = False
ACCOUNT_REQUIRED_EMAIL = False
ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = False
ACCOUNT_LOGIN_REDIRECT_URL = "home"
ACCOUNT_LOGOUT_REDIRECT_URL = "home"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 2

AUTHENTICATION_BACKENDS = [
    "account.auth_backends.UsernameAuthenticationBackend",
]


SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'



FILE_UPLOAD_MAX_MEMORY_SIZE = '2621440'
#FILE_UPLOAD_TEMP_DIR = os.path.join(PROJECT_ROOT, "tmp")

