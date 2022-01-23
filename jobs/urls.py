from django.urls import path

from jobs import views


urlpatterns = [
    # Django 4.x 不支持 url
    path("joblist/", views.joblist, name="joblist"),
    path('job/<int:job_id>/', views.detail, name='detail'),
]
