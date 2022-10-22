from .base import *

ALLOWED_HOSTS = ["recruit.ihopeit.com", "127.0.0.1"]

# LDAP
LDAP_AUTH_URL = "ldap://127.0.0.1:389"
LDAP_AUTH_CONNECTION_USERNAME = "admin"
LDAP_AUTH_CONNECTION_PASSWORD = "123456"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-f(_1+j7ic5n30-30e60=_e80x6g(=*+qg4nqc$t!smm^$*-6#o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

INSTALLED_APPS += (
    # 'debug_toolbar'
)
