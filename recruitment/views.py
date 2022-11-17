from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy

from captcha.fields import CaptchaField
from ratelimit.decorators import ratelimit

import logging

logger = logging.getLogger(__name__)


class CaptchaLoginForm(AuthenticationForm):
    # username = forms.CharField(label='用户名')
    # password = forms.CharField(widget=forms.PasswordInput, label='密码')
    captcha = CaptchaField(label='验证码')


max_failed_login_count = 3


# 按 IP 限制，每个 IP 每分钟最多 5 次访问
@ratelimit(key='ip', rate='5/m', block=True)
def login_with_captcha(request):
    if request.POST:
        failed_login_count = request.session.get('failed_login_count', 0)

        # 没有连续的登录失败，使用默认登录页；连续 n 次登录失败，要求输入验证码
        if failed_login_count >= max_failed_login_count:
            form = CaptchaLoginForm(data=request.POST)
        else:
            form = AuthenticationForm(data=request.POST)

        # Validate the form: the captcha field will automatically
        # check the input
        if form.is_valid():
            request.session['failed_login_count'] = 0
            # authenticate user with credentials
            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            if user is not None:
                # attach the authenticated user to the current session
                login(request, user)
                # 返回 admin 的首页
                return HttpResponseRedirect(reverse_lazy('admin:index'))
        else:
            failed_login_count += 1
            request.session['failed_login_count'] = failed_login_count
            logger.warning("---- failed login for user: %s, failed times: %s"
                           % (form.data["username"], failed_login_count))
            if failed_login_count >= max_failed_login_count:
                form = CaptchaLoginForm(request.POST)
            messages.add_message(request, messages.INFO, "Not a valid request")
    else:
        # 判断 GET 请求，输入 URL 直接访问
        failed_login_count = request.session.get('failed_login_count', 0)
        if failed_login_count >= max_failed_login_count:
            form = CaptchaLoginForm(request.POST)
        else:
            form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
