"""
Local settings
"""

from base import *

DEBUG = True

SITE_ID = 1
STATIC_URL = '/static/'
SITE_URL = 'herdit.co.uk'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Enable web-browser session auth
REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'].append(
    'rest_framework.authentication.SessionAuthentication')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Scoped throttles to use
REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = ({})
REST_FRAMEWORK['DEFAULT_THROTTLE_CLASSES'] = ({})

###########################################################
# Logging
###########################################################

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s]: %(asctime)s [%(pathname)s:%(lineno)s] [pid:%(process)d] [thread:%(thread)d] %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/logs/django_error.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.request': {
            'level': 'DEBUG',
            'handlers': ['file'],
            'propagate': False,
        },
        'django.db.backends': {
            'level': 'INFO',
            'handlers': ['file'],
            'propagate': False,
        },
        SITE_NAME: {
            'level': 'DEBUG',
            'handlers': ['file'],
            'propagate': False,
        },
    },
}
