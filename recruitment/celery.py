# 避免导入的包有命名冲突
# from __future__ import absolute_import, unicode_literals

import os
import json

# from django_celery_beat.models import PeriodicTask, IntervalSchedule

from celery import Celery
from celery.schedules import crontab

# from recruitment.tasks import add

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.base')

app = Celery('recruitment')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


# 系统启动后执行任务
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, test.s('hello'), name='hello every 10')

    sender.add_periodic_task(30.0, test.s('world'), expires=10)

    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )


@app.task
def test(arg):
    print(arg)


# 直接配置定时任务
app.conf.beat_schedule = {
    'add-every-10-seconds': {
        'task': 'recruitment.tasks.add',
        'schedule': 10.0,
        'args': (16, 4,)
    },
}

# # 动态添加任务：先创建定时策略
# schedule, created = IntervalSchedule.objects.get_or_create(every=10, period=IntervalSchedule.SECONDS,)
#
# # 动态添加任务：再创建任务
# task = PeriodicTask.objects.create(interval=schedule, name='say welcome 2022', task='recruitment.celery.test',
#                                    args=json.dumps(['welcome']),)
#
#
# @app.task
# def test(arg):
#     print(arg)
#
#
# app.conf.timezone = 'Asia/Shanghai'
