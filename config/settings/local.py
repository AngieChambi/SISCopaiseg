from .base import *

INSTALLED_APPS += [
    "coverage",
    'debug_toolbar',
    "docutils",
]

MIDDLEWARE_CLASSES += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',

]
DATABASESs = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'clivet_db',
        'USER': 'clivetclouduser',
        'PASSWORD': 'clivet_admin_74732460',
        'HOST': '35.192.58.187',
        'PORT': '',
    }
}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DATABASESm = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # sqlite3
        'NAME': 'db2',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}



# DESC
DESC = 'DESC'
if DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
    DESC = 'ASC'



def show_toolbar(request):
    if not request.is_ajax() and request.user:
        return True
    return False


if DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, '/static')
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')


STATIC_URL = '/static/'
# Additional locations of static files
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
