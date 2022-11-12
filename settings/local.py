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

# Redis
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:16379/1",
        "TIMEOUT": 300,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # "PASSWORD": "123456",
            # Redis 连接超时时间，单位 s
            "SOCKET_CONNECT_TIMEOUT": 5,
            # 每次读取数据超时时间，单位 s
            "SOCKET_TIMEOUT": 5,
        }
    }
}

# Celery application definition
CELERY_BROKER_URL = 'redis://127.0.0.1:16379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:16379/1'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_MAX_TASKS_PER_CHILD = 10
CELERY_LOG_FILE = os.path.join(BASE_DIR, "logs", "celery_work.log")
CELERYBEAT_LOG_FILE = os.path.join(BASE_DIR, "logs", "celery_beat.log")

# OSS
# STATIC_URL = 'http://xxx/static/'
# DEFAULT_FILE_STORAGE = 'django_oss_storage.backends.OssMediaStorage'
# OSS_ACCESS_KEY_ID = 'LTAI4GFtQd78UtDhfZUtUAs4'
# OSS_ACCESS_KEY_SECRET = 'eTS9T3FfZaBFdtfprzjrxVMacw1Cc7'
# OSS_BUCKET_NAME = 'djangorecruit'
# OSS_ENDPOINT = 'oss-cn-beijing.aliyuncs.com'
