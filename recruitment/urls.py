"""recruitment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# Django 中多语言环境一般用 "_" 来作为函数名
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import routers, serializers, viewsets

from jobs.models import Job
from recruitment import views


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class JobSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'


class JobViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows group to be viewed or edited.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'jobs', JobViewSet)

urlpatterns = [
    path("", include("jobs.urls")),
    path("grappelli/", include("grappelli.urls")),

    # 使用 login_with_captcha 作为管理员的登陆页
    path('admin/login/', views.login_with_captcha, name='adminlogin'),

    path('admin/', admin.site.urls),
    path('accounts/', include('registration.backends.simple.urls')),

    # rest api & api auth(login logout)
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),

    # prometheus
    path('', include('django_prometheus.urls')),

    # captcha
    path('captcha/', include('captcha.urls')),
    path('clogin/', views.login_with_captcha, name="clogin"),

]

# Debug
if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))


# document_root 设置到 MEDIA_URL 下，并加到 urlpatterns
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = _('酱油科技-招聘管理系统')
