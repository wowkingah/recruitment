from django.contrib import admin
from django.apps import apps, AppConfig


class ListAdminMixin(object):
    def __init__(self, model, admin_site):
        # 列表面自动显示所有字段
        self.list_display = [field.name for field in model._meta.fields]
        super(ListAdminMixin, self).__init__(model, admin_site)


class UniversalManagerApp(AppConfig):
    """
    应用配置在所有应用的 Admin 都加载完之后执行
    """
    name = 'recruitment'

    # recruitment 应用加载完之后调用 ready 方法
    def ready(self):
        models = apps.get_app_config('running').get_models()
        for model in models:
            admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
            try:
                admin.site.register(model, admin_class)
            # pass 已注册过的 model
            except admin.sites.AlreadyRegistered:
                pass
