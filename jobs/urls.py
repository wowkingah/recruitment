from django.urls import path

from jobs import views


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

]
