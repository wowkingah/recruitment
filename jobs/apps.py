from django.apps import AppConfig

import logging

logger = logging.getLogger(__name__)


class JobsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jobs'

    def ready(self):
        logger.info("JobConfig ready")
        # jobs 应用加载完之后，注册信号量处理器，把 post_save_callback 加载到 Django 的运行框架中
        # from jobs.signal_processor import post_save_callback
