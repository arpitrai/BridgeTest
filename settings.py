# Testing
# Django settings for bridgebill project.
import os.path
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

# For Production specific values
import socket
if socket.gethostname() == 'Arpits-MacBook-Air-2.local':
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
else:
    DEBUG = False
    TEMPLATE_DEBUG = DEBUG
    #PREPEND_WWW = True # Required for Facebook Connect which works only on the domain with the www

ADMINS = (
    # ('arprai', 'arprai@deloitte.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'bridgebill',                      # Or path to database file if using sqlite3.
        'USER': os.environ['BRIDGE_DB_USERNAME'],                      # Not used with sqlite3.
        'PASSWORD': os.environ['BRIDGE_DB_PASSWORD'],                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Start - Heroku Database Setting
if socket.gethostname() != 'Arpits-MacBook-Air-2.local':
    #import dj_database_url
    #DATABASES['default'] =  dj_database_url.config()
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
			'NAME': 'bridgebill',                      # Or path to database file if using sqlite3.
			'USER': 'postgres',                      # Not used with sqlite3.
			'PASSWORD': '',                  # Not used with sqlite3.
			'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
			'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
		}
	}
# End - Heroku Database Setting

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Singapore'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
if socket.gethostname() == 'Arpits-MacBook-Air-2.local':
    STATIC_ROOT = os.path.join(PROJECT_PATH, 'staticfiles') 
else:
    STATIC_ROOT = 'http://bridgebill.s3-website-ap-southeast-1.amazonaws.com/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
if socket.gethostname() == 'Arpits-MacBook-Air-2.local':
    STATIC_URL = '/static/'
else: 
    STATIC_URL = 'http://s3-ap-southeast-1.amazonaws.com/bridgebill/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

# Additional locations of static files
STATICFILES_DIRS = (
        os.path.join(PROJECT_PATH, 'bridgebill/static'), 
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '$*56$60abst*_1ey$(44e^78wwamr7gi)vin&^zq+!rbkdv4eh'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
        os.path.join(PROJECT_PATH, 'bridgebill/templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'bridgebill',
    'social_auth',
    'storages',
    'gunicorn',
    'django.contrib.humanize',
    'mailer',
    'south',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Start - Amazon S3 storage settings
DEFAULT_FILE_STORAGE    = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID       = os.environ['BRIDGE_AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY   = os.environ['BRIDGE_AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['BRIDGE_AWS_STORAGE_BUCKET_NAME']
from S3 import CallingFormat
AWS_CALLING_FORMAT      = CallingFormat.SUBDOMAIN
STATICFILES_STORAGE     = 'storages.backends.s3boto.S3BotoStorage' 
# End - Amazon S3 storage settings

# Start - UserProfile Model
AUTH_PROFILE_MODEL = 'bridgebill.UserProfile'
# End - UserProfile Model

# Start - Admin Email 
DEFAULT_FROM_EMAIL = 'BridgeBill <admin@bridgebill.com>'
# End - Admin Email 

# Start - Sending Emails through Amazon SES
EMAIL_HOST          = os.environ['BRIDGE_EMAIL_HOST']
EMAIL_HOST_USER     = os.environ['BRIDGE_EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['BRIDGE_EMAIL_HOST_PASSWORD']
EMAIL_PORT          = 25
EMAIL_USE_TLS       = True
# End - Sending Emails through Amazon SES


# Start - Facebook Connect
AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'django.contrib.auth.backends.ModelBackend',
)

if socket.gethostname() == 'Arpits-MacBook-Air-2.local':
    FACEBOOK_APP_ID              = os.environ['BRIDGE_DEV_FACEBOOK_APP_ID']
    FACEBOOK_API_SECRET          = os.environ['BRIDGE_DEV_FACEBOOK_API_SECRET']
else:
    FACEBOOK_APP_ID              = os.environ['BRIDGE_PROD_FACEBOOK_APP_ID']
    FACEBOOK_API_SECRET          = os.environ['BRIDGE_PROD_FACEBOOK_API_SECRET']

FACEBOOK_EXTENDED_PERMISSIONS = ['email']
# End - Facebook Connect

# Start - For Django Social Auth
LOGIN_URL          = '/'
LOGIN_REDIRECT_URL = '/home/'
LOGIN_ERROR_URL    = '/login-error/'

SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'

SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'

SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email',]
# End - For Django Social Auth
