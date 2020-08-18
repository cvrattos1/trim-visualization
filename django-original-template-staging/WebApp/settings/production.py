from WebApp.settings.base import *
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['MYSQL_DATABASE'],
        'USER': os.environ['MYSQL_USER'],
        'PASSWORD': os.environ['MYSQL_ROOT_PASSWORD'],
        'HOST': os.environ['MYSQL_CONTAINER_NAME'],
        'PORT': os.environ['MYSQL_PORT']
    }
}

# Production overrides
DEBUG = os.environ['DJANGO_DEBUG']
