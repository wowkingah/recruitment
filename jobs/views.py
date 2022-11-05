from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView

from jobs.models import Job, Resume
from jobs.models import Cities, JobTypes

import html

# Create your views here.

def joblist(request):
    job_list = Job.objects.order_by('job_type')
    # template = loader.get_template('joblist.html')
    context = {'job_list': job_list}

    for job in job_list:
        job.city_name = Cities[job.job_city][1]
        job.type_name = JobTypes[job.job_type][1]

    # return HttpResponse(template.render(context))
    return render(request, 'joblist.html', context)


def detail(request, job_id):
    try:
        job = Job.objects.get(pk=job_id)
        job.city_name = Cities[job.job_city][1]
    except Job.DoesNotExist:
        raise Http404("Job does not exits.")

    return render(request, 'job.html', {'job': job})


# 直接返回 HTML 内容的视图（这段代码返回的页面有 XSS 漏洞，能够被攻击者利用）
def detail_resume(request, resume_id):
    try:
        resume = Resume.objects.get(pk=resume_id)
        content = "name: %s <br> introduction: %s <br>" % (resume.username, resume.candidate_introduction)
        # return HttpResponse(content)
        # 使用 html.escape 将 content 内容转义（建议使用 render 替代）
        return HttpResponse(html.escape(content))
    except Resume.DoesNotExist:
        raise Http404("resume does not exist")


# 类只能继承一个父类，Mixin 可实现一个类能继承多个类
class ResumeCreateView(LoginRequiredMixin, CreateView):
    """ 简历职位页面 """
    template_name = 'resume_form.html'
    success_url = '/joblist/'
    model = Resume
    fields = ["username", "city", "phone",
              "email", "apply_position", "gender",
              "bachelor_school", "master_school", "major", "degree",
              "candidate_introduction", "work_experience", "project_experience"]

    # 从 URL 请求参数带入默认值
    def get_initial(self):
        initial = {}
        for x in self.request.GET:
            initial[x] = self.request.GET[x]
        return initial

    # 简历跟当前用户关联
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.applicant = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ResumeDetailView(DetailView):
    """ 简历详情页 """
    model = Resume
    template_name = 'resume_detail.html'

