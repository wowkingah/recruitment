from django.contrib import admin
from django.http import HttpResponse

from interview.models import Candidate

import logging
import csv
from datetime import datetime

# Register your models here.

# 使用当前运行的脚本名
logger = logging.getLogger(__name__)

# 定义导出字段列表
exportable_fields = ('username', 'city', 'phone', 'bachelor_school', 'master_school', 'degree', 'first_result',
                     'first_interviewer', 'second_result', 'second_interviewer', 'hr_result', 'hr_score', 'hr_remark',
                     'hr_interviewer')


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
    logger.info("%s exported %s candidate records" % (request.user.username, len(queryset)))

    return response


# 自定义导出菜单显示名
export_model_as_csv.short_description = u'导出为CSV文件'


# 候选人管理类
class CandidateAdmin(admin.ModelAdmin):
    exclude = ('creator', 'created_date', 'modified_date')

    # 导出函数注册到 actions
    actions = [export_model_as_csv, ]

    # 显示字段
    list_display = (
        "username", "city", "bachelor_school", "first_score", "first_result", "first_interviewer",
        "second_result", "second_interviewer", "hr_score", "hr_result", "last_editor"
    )

    # 筛选条件
    list_filter = ('city', 'first_result', 'second_result', 'hr_result', 'first_interviewer',
                   'second_interviewer', 'hr_interviewer')

    # 查询字段
    search_fields = ('username', 'phone', 'email', 'bachelor_school')

    # 排序字段
    ordering = ('hr_result', 'second_result', 'first_result')

    # 分组显示
    fieldsets = (
        (None, {'fields': ("userid", ("username", "city", "phone"), ("email", "apply_position", "born_address"),
                           ("gender", "candidate_remark"), ("bachelor_school", "master_school", "doctor_school"),
                           ("major", "degree"), ("test_score_of_general_ability", "paper_score"), "last_editor",)}),
        ('第一轮面试记录', {'fields': (("first_score", "first_learning_ability", "first_professional_competency"),
                                       "first_advantage", "first_disadvantage", "first_result",
                                       "first_recommend_position",
                                       "first_interviewer", "first_remark",)}),
        (
            '第二轮专业复试记录',
            {'fields': (("second_score", "second_learning_ability", "second_professional_competency"),
                        ("second_pursue_of_excellence", "second_communication_ability",
                         "second_pressure_score"), "second_advantage", "second_disadvantage",
                        "second_result",
                        "second_recommend_position", "second_interviewer", "second_remark",)}),
        ('HR复试记录', {'fields': ("hr_score", ("hr_responsibility", "hr_communication_ability", "hr_logic_ability"),
                                   ("hr_potential", "hr_stability"), "hr_advantage", "hr_disadvantage", "hr_result",
                                   "hr_interviewer", "hr_remark",)}),
    )


admin.site.register(Candidate, CandidateAdmin)
