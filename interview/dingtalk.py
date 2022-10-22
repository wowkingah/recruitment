# coding=utf-8
from dingtalkchatbot.chatbot import DingtalkChatbot

from django.conf import settings


def send(message, at_mobiles=[]):
    # 引用 settings 里配置的钉钉群消息通知的 WebHook 地址
    webhook = settings.DINGTALK_WEB_HOOK

    # 初始化机器人小丁，# 方式一：通常初始化
    xiaoding = DingtalkChatbot(webhook)

    # 方式二：勾选 “加签” 选项时使用（v1.5 以上新功能）
    # xiaoding = DingtalkChatbot(webhook, secret=secret)

    # Text 消息 @所有人
    xiaoding.send_text(msg=('面试通知：%s' % message), at_mobiles=at_mobiles)
