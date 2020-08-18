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


DEBUG = os.environ['DJANGO_DEBUG']

if DEBUG:

    def show_toolbar(request):
        if request.is_ajax():
            return False
        return True

    INSTALLED_APPS += (
        'debug_toolbar',
        'django_uwsgi',
    )
    
    # INTERNAL_IPS = ('192.168.99.100', '192.168.99.101')
    
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        'SHOW_TOOLBAR_CALLBACK': 'WebApp.settings.local.show_toolbar',
    }

    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
        'django_uwsgi.panels.UwsgiPanel',
    ]
# end django-debug-toolbar
