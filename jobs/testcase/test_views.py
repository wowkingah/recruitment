from django.test import TestCase
from django.test import Client

from jobs.models import Job, JobTypes, Cities


class JobTests(TestCase):
    # 加载类时会做准备工作，会在该类下创建一个 job 对象
    @classmethod
    def setUpTestData(cls):
        # set up data for the whole TestCase
        cls.job = Job.objects.create(job_name="dba", job_type=JobTypes[0][0], job_city=Cities[1][0], job_requirement="sql")
        # cls.job = Job.objects.create(job_name="Java 开发工程师", job_type=JobTypes[0][0],
        #                              job_city=Cities[1][0], job_requirement="精通Java开发")

    def test1(self):
        # some test using self.job
        pass

    # 测试职位发布后，首页访问是否正常
    def test_index(self):
        client = Client()
        response = client.get('/joblist/')
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        # 使用 TestCase.self.client 作为 HTTP Client
        response = self.client.get('/job/1/')
        self.assertEqual(response.status_code, 200)

        job = response.context['job']
        self.assertEqual(job.job_name, JobTests.job.job_name)
