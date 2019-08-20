# -*- coding: utf-8 -*-
"""
Django settings for ecocharte project.

Generated by 'django-admin startproject' using Django 1.8.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/

 python manage.py createsuperuser
python manage.py migrate --run-syncdb

"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

try:
    import dj_database_url
except:
    pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!


# SECURITY WARNING: don't run with debug turned on in production!
try:
    LOCALL = False
    DEBUG = False
    SECRET_KEY = os.environ['SECRET_KEY']
    ALLOWED_HOSTS = ['ecocharte.herokuapp.com']
except:
    LOCALL  = True
    SECRET_KEY = 'aersd68fgsfdgsdvcbvcb563873gbgfthhfhdjd'
    DEBUG = True

    ALLOWED_HOSTS = ['127.0.0.1']


#SECURE_SSL_REDIRECT = False
#SESSION_COOKIE_SECURE = True
#CSRF_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE=True


# Application definition

# pip install django-fontawesome django-model_utils django-debug_toolbar django-haystack django-bootstrap django-extensions django-leaflet django-filter django-rest-framework django-scheduler django-widget-tweaks

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    'django.contrib.sites',
    'bootstrap','fontawesome','cookielaw',
    'model_utils',
    'ecocharte',
    'django_extensions',
    'django_filters',
    'widget_tweaks',
    'leaflet',
    'captcha',
    'django_summernote',
)


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
     'django.middleware.locale.LocaleMiddleware',
]


ROOT_URLCONF = 'ecocharte.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
            ],
            'string_if_invalid': 'Invalid: "%s"',
        },
    },
]


WSGI_APPLICATION = 'ecocharte.wsgi.application'
# Database
if LOCALL:
    DATABASES = {
       'default': {
          'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.db'),
        }
    }
    ALLOWED_HOSTS = ['127.0.0.1']
else:
    DATABASES = dict()
    DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)


# except:


AUTH_PASSWORD_VALIDATORS = [
    #{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    #{    'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    #{'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    #{'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

HAYSTACK_CONNECTIONS = {
  'default': {
    'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
    'PATH': os.path.join(os.path.dirname(__file__), 'search_index'),
  },
}
AUTH_USER_MODEL = 'ecocharte.Profil'
# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

SITE_ID = 1

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATE_FORMAT = "l d F Y"
DATE_FORMAT_COURT = "d F Y"
DATE_FORMAT_COURT_HEURE = "d F Y, G:i"
#DATETIME_INPUT_FORMATS = '%d/%m/%Y'
#TIME_INPUT_FORMATS = '%H:%M'
SHORT_DATE_FORMAT = "d F Y"
#DATE_INPUT_FORMATS = ('%d/%m/%Y',)


LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

INTERNAL_IPS = ['127.0.0.1']

########################
import re
IGNORABLE_404_URLS = (
    re.compile('\.(php|cgi)$'),
    re.compile('^/phpmyadmin/'),
    re.compile('^/apple-touch-icon.*\.png$'),
    re.compile('^/favicon\.ico$'),
    re.compile('^/robots\.txt$'),
)

# Email settings
SERVER_EMAIL = 'ecocharte.cat@gmail.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
try:
    EMAIL_HOST_PASSWORD = os.environ['EMAIL_ADMIN_PWD']
except:
    EMAIL_HOST_PASSWORD = 'gg'
EMAIL_HOST_USER = SERVER_EMAIL
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
GMAIL_SMTP_USER = 'ecocharte.cat@gmail.com'
EMAIL_SUBJECT_PREFIX = "[EcoCharte]"
try:
    GMAIL_SMTP_PASSWORD = os.environ['EMAIL_ADMIN_PWD']
except:
    GMAIL_SMTP_PASSWORD = 'test'

ADMINS = (
    ('Asso_admin', 'ecocharte.cat@gmail.com'),
)
MANAGERS = ADMINS
BASE_URL = "https://ecocharte.herokuapp.com"
########################
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

if LOCALL:
    STATICFILES_DIRS = (os.path.normpath(os.path.join(BASE_DIR, 'staticfiles/')), )
    STATIC_ROOT = os.path.normpath(os.path.join(BASE_DIR, 'static/'))

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.normpath(os.path.join(BASE_DIR, '/media/'))

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# LOCATION_FIELD = {
#     'map.provider': 'openstreetmap',
# }


LEAFLET_CONFIG = {
'DEFAULT_CENTER': (42.7201813, 2.8876436),
'DEFAULT_ZOOM': 10,
'MIN_ZOOM': 3,
'MAX_ZOOM': 18,
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

PHONENUMBER_DEFAULT_REGION = 'EUROPE'

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)

gettext =  lambda x: x
LANGUAGES = (
   ('fr', gettext('French')),
   ('ca', gettext('Catalan')),
)

SUMMERNOTE_CONFIG = {
    # Using SummernoteWidget - iframe mode, default
    'iframe': True,

    # Or, you can set it as False to use SummernoteInplaceWidget by default - no iframe mode
    # In this case, you have to load Bootstrap/jQuery stuff by manually.
    # Use this when you're already using Bootstraip/jQuery based themes.
    #'iframe': False,

    # You can put custom Summernote settings
    'summernote': {

        # As an example, using Summernote Air-mode
        'airMode': False,

        # Change editor size
        'width': '100%',
        'height': '480',

        # Use proper language setting automatically (default)
        'lang': 'fr-FR',
},
"toolbar": [
    ['style', ['bold', 'italic', 'underline', 'clear']],
    ['fontsize', ['fontsize']],
    ['fontSizes', ['8', '9', '10', '11', '12', '14', '18', '22', '24', '36']],
    ['color', ['color']],
    ['para', ['ul', 'ol', 'paragraph']],
    ['link', ['link', 'picture', 'video', 'table', 'hr',]],
    ['misc', [ 'undo', 'redo', 'help','fullscreen', 'codeview',  'readmore']],

],
"popover": {
  "image": [
    ['imagesize', ['imageSize100', 'imageSize50', 'imageSize25']],
    ['float', ['floatLeft', 'floatRight', 'floatNone']],
    ['remove', ['removeMedia']]
  ],
  "link": [
    ['link', ['linkDialogShow', 'unlink']]
  ],
  "air": [
    ['color', ['color']],
    ['font', ['bold', 'underline', 'clear']],
    ['para', ['ul', 'paragraph']],
    ['table', ['table']],
    ['insert', ['link', 'picture']]
  ]
},


# Need authentication while uploading attachments.
'attachment_require_authentication': True,

# You can disable attachment feature.
'disable_attachment': True,

# Set `True` to return attachment paths in absolute URIs.
'attachment_absolute_uri': False,

# You can add custom css/js for SummernoteWidget.
'css': (
),
'js': (
),

# You can also add custom css/js for SummernoteInplaceWidget.
# !!! Be sure to put {{ form.media }} in template before initiate summernote.
'css_for_inplace': (
),
'js_for_inplace': (
),

# Codemirror as codeview
# If any codemirror settings are defined, it will include codemirror files automatically.
'css': (
    '//cdnjs.cloudflare.com/ajax/libs/codemirror/5.29.0/theme/monokai.min.css',
),
'codemirror': {
    'mode': 'htmlmixed',
    'lineNumbers': 'true',

    # You have to include theme file in 'css' or 'css_for_inplace' before using it.
    'theme': 'monokai',
},

# Lazy initialize
# If you want to initialize summernote at the bottom of page, set this as True
# and call `initSummernote()` on your page.
'lazy': True,

# To use external plugins,
# Include them within `css` and `js`.
#'js': {
#},
}


#if not LOCALL:
#    import django_heroku
#    django_heroku.settings(locals())

SECURE_HSTS_SECONDS = 518400
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT  = True
SESSION_COOKIE_SECURE  = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'