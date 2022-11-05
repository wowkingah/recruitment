from .base import *

ALLOWED_HOSTS = ["recruit.ihopeit.com", "127.0.0.1"]

# LDAP
LDAP_AUTH_URL = "ldap://127.0.0.1:389"
LDAP_AUTH_CONNECTION_USERNAME = "admin"
LDAP_AUTH_CONNECTION_PASSWORD = "123456"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-f(_1+j7ic5n30-30e60=_e80x6g(=*+qg4nqc$t!smm^$*-6#o'

# DINGTALK
DINGTALK_WEB_HOOK = "https://oapi.dingtalk.com/robot/send?access_token=xxx"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

INSTALLED_APPS += (
    # 'debug_toolbar'
)

# sentry
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="http://ebc94be7ebd548d2bcbcf86bc3b2300e@127.0.0.1:9000/2",
    integrations=[
        DjangoIntegration(),
    ],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)
