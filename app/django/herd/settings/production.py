"""
Production settings
"""

from base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']
SITE_URL = 'www.herdit.co.uk'

########################################################################
# KEY/VALUES
########################################################################

# Place in Try/Except to crash at load time rather than run time.
try:

    # AWS Credentials
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

    # S3 Bucket Name
    S3_STATIC_FILES_BUCKET_NAME = os.environ['S3_STATIC_FILES_BUCKET_NAME']

except KeyError, e:
    print "ERROR: Unable to load AWS environment variable: %s" % e
    print "Have you 'sourced' in the keys?"
    exit(1)

###########################################################
# Django Settings
###########################################################

INSTALLED_APPS += (
    'storages',  # AWS
)

###########################################################
# Django Rest Framework
###########################################################

# Scoped throttles to use
REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = ({
    'login': '5/hour',
    'password_reset': '5/hour',
    'change_password': '5/hour',
    'change_email': '5/hour',
    'general': '20/minute',
})

# Disable browseable REST API
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
    'rest_framework.renderers.JSONRenderer']


###########################################################
# AWS S3
###########################################################

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_STORAGE_BUCKET_NAME = S3_STATIC_FILES_BUCKET_NAME

S3_STATIC_FILES_URL = 'https://%s.s3.amazonaws.com/' % S3_STATIC_FILES_BUCKET_NAME
STATIC_URL = S3_STATIC_FILES_URL

###########################################################
# Email backend service
###########################################################

EMAIL_BACKEND = 'django_ses.SESBackend'

AWS_SES_REGION_NAME = 'eu-west-1'
AWS_SES_REGION_ENDPOINT = 'email.eu-west-1.amazonaws.com'

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
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/logs/django_error.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.request': {
            'level': 'WARNING',
            'handlers': ['file'],
            'propagate': False,
        },
        'django.db.backends': {
            'level': 'WARNING',
            'handlers': ['file'],
            'propagate': False,
        },
        SITE_NAME: {
            'level': 'INFO',
            'handlers': ['file'],
            'propagate': False,
        },
    },
}
