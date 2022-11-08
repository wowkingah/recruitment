from django.contrib import admin
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from django.utils.safestring import mark_safe

from interview.models import Candidate
from interview import candidate_fieldset as cf
from interview import dingtalk
from jobs.models import Resume
from .tasks import send_dingtalk_message

import logging
import csv
from datetime import datetime

# Register your models here.

# 使用当前运行的脚本名
logger = logging.getLogger(__name__)

# 定义导出字段列表
exportable_fields = ('username', 'city', 'phone', 'bachelor_school', 'master_school', 'degree', 'first_result',
                     'first_interviewer_user', 'second_result', 'second_interviewer_user', 'hr_result', 'hr_score',
                     'hr_remark', 'hr_interviewer_user')


def export_model_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    field_list = exportable_fields
    # 将 response['Content-Disposition'] 设置为字符串，内容为 attachment
    response['Content-Disposition'] = 'attachment; filename=recruitment-candidates-list-%s.csv' % (
        datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
    )

    # 写入表头
    writer = csv.writer(response)
    # 定义表头，将字段中每列的英文名转成中文名显示
    writer.writerow(
        [queryset.model._meta.get_field(f).verbose_name.title() for f in field_list]
    )

    for obj in queryset:
        # 单行的记录（各字段的值），写到 csv 文件
        csv_line_values = []
        for field in field_list:
            field_object = queryset.model._meta.get_field(field)
            field_value = field_object.value_from_object(obj)
            csv_line_values.append(field_value)
        writer.writerow(csv_line_values)

    # 导出 csv 时，记录日志
    # logger.info("%s exported %s candidate records" % (request.user.username, len(queryset)))
    logger.error("%s has exported %s candidate records" % (request.user.username, len(queryset)))

    return response


# 自定义导出菜单显示名
export_model_as_csv.short_description = u'导出为CSV文件'
export_model_as_csv.allowed_permissions = ("export",)


# 通知一面面试官面试
def notify_interviewer(modeladmin, request, queryset):
    candidates = ""
    interviewers = ""
    for obj in queryset:
        candidates = obj.username + ";" + candidates
        interviewers = obj.first_interviewer_user.username + ";" + interviewers
    # dingtalk.send("候选人 %s 进入面试环节，亲爱的面试官，请准备好面试：%s" % (candidates, interviewers))
    send_dingtalk_message.delay("候选人 %s 进入面试环节，亲爱的面试官，请准备好面试：%s" % (candidates, interviewers))
    messages.add_message(request, messages.INFO, '已成功发送面试通知')


notify_interviewer.short_description = u'通知一面面试官'


# 候选人管理类
class CandidateAdmin(admin.ModelAdmin):
    exclude = ('creator', 'created_date', 'modified_date')

    # 导出函数注册到 actions
    actions = [export_model_as_csv, notify_interviewer]

    # 当前用户是否有导出权限
    def has_export_permission(self, request):
        opts = self.opts
        return request.user.has_perm('%s.%s' % (opts.app_label, "export"))

    # 显示字段
    list_display = (
        "username", "city", "bachelor_school", "get_resume", "first_score", "first_result", "first_interviewer_user",
        "second_result", "second_interviewer_user", "hr_score", "hr_result", "last_editor"
    )

    # 筛选条件
    list_filter = ('city', 'first_result', 'second_result', 'hr_result', 'first_interviewer_user',
                   'second_interviewer_user', 'hr_interviewer_user')

    # 查询字段
    search_fields = ('username', 'phone', 'email', 'bachelor_school')

    # 排序字段
    ordering = ('hr_result', 'second_result', 'first_result')

    # 只读字段
    # readonly_fields = ('first_interviewer_user', 'second_interviewer_user')
    def get_group_names(self, user):
        group_names = []
        for g in user.groups.all():
            group_names.append(g.name)
        return group_names

    def get_readonly_fields(self, request, obj):
        group_names = self.get_group_names(request.user)

        if 'interviewer' in group_names:
            logger.info("interviewer is in user's group for %s" % request.user.username)
            return 'first_interviewer_user', 'second_interviewer_user',
        return ()

    # 编辑字段
    default_list_editable = ("first_interviewer_user", "second_interviewer_user")

    def get_list_editable(self, request):
        group_names = self.get_group_names(request.user)

        if request.user.is_superuser or 'hr' in group_names:
            return self.default_list_editable
        return ()

    # 因 Django 中未内置 get_list_editable 函数，可通过覆盖 ModelAdmin 父类里 get_changelist_instance 方法的 list_editable 属性
    def get_changelist_instance(self, request):
        self.list_editable = self.get_list_editable(request)
        return super(CandidateAdmin, self).get_changelist_instance(request)

    # 定制面试官权限：一面面试官仅可填写一面反馈，二面面试官仅可填写二面反馈
    def get_fieldsets(self, request, obj=None):
        group_names = self.get_group_names(request.user)

        if 'interviewer' in group_names and obj.first_interviewer_user == request.user:
            return cf.default_fieldsets_first
        if 'interviewer' in group_names and obj.second_interviewer_user == request.user:
            return cf.default_fieldsets_second
        return cf.default_fieldsets

    # 对于非管理员、非HR，获取自己是一面面试官或者二面面试官的候选人集合:s
    def get_queryset(self, request):
        qs = super(CandidateAdmin, self).get_queryset(request)

        group_names = self.get_group_names(request.user)
        if request.user.is_superuser or 'hr' in group_names:
            return qs
        return Candidate.objects.filter(
            # Q 表达式，可用来做 or 或 and 的复杂查询
            Q(first_interviewer_user=request.user) | Q(second_interviewer_user=request.user)
        )

    def get_resume(self, obj):
        if not obj.phone:
            return ""
        resumes = Resume.objects.filter(phone=obj.phone)
        if resumes and len(resumes) > 0:
            return mark_safe(u'<a href="/resume/%s" target="_blank">%s</a' % (resumes[0].id, "查看简历"))
        return ""

    get_resume.short_description = u'查看简历'
    # 使用 HTML 标签
    get_resume.allow_tags = True


admin.site.register(Candidate, CandidateAdmin)
