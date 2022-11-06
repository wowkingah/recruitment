#!coding=utf-8

from celery import Celery

# 第一个参数是当前脚本的名称，第二个参数为 broker 服务地址
# backend：存储每个异步任务的结果，可以是 Redis 或 DB 等；broker：存储任务
app = Celery('tasks', backend='redis://127.0.0.1:16379', broker='redis://127.0.0.1:16379')


@app.task
def add(x, y):
    return x + y
