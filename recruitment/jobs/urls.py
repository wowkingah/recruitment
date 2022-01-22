from django.urls import path

from jobs import views


urlpatterns = [
    # 职位列表
    path("joblist/", views.joblist, name="joblist"),
    path('job/<int:job_id>/', views.detail, name='detail'),
]
