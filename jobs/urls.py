from django.urls import path
from django.conf.urls import include

from jobs import views


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    # Django 4.x+ 不支持 url
    path("joblist/", views.joblist, name="joblist"),
    path('job/<int:job_id>/', views.detail, name='detail'),

    # 提交简历
    path("resume/add/", views.ResumeCreateView.as_view(), name='resume-add'),
    # <int:pk>：引用主键
    path("resume/<int:pk>/", views.ResumeDetailView.as_view(), name='resume-detail'),

    # 首页自动跳转到职位列表
    path("", views.joblist, name="name"),

    # 多语言URL 路径
    path('i18n/', include('django.conf.urls.i18n')),

    # sentry-debug
    path('sentry-debug/', trigger_error),
]
