import time
import logging

from django.http import HttpResponse
import traceback

from sentry_sdk import capture_exception, capture_message
from . import dingtalk

logger = logging.getLogger(__name__)


def performance_logger_middleware(get_response):
    def middleware(request):
        start_time = time.time()
        response = get_response(request)
        duration = time.time() - start_time
        # 通过 response 头返回，访问页面时通过浏览器 Inspect 工具可看到
        response["X-Page-Duration-ms"] = int(duration * 1000)
        logger.info("%s %s %s", duration, request.path, request.GET.dict())
        return response

    return middleware


class PerformanceAndExceptionLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time
        response["X-Page-Duration-ms"] = int(duration * 1000)
        logger.info("duration:%s url:%s parameters:%s", duration, request.path, request.GET.dict())

        if duration > 300:
            capture_message("slow request for url:%s with duration:%s" % (request.path, request.GET.dict()))

        return response

    def process_exception(self, request, exception):
        if exception:
            message = "url:{url} ** msg:{error} ````{tb}````".format(
                url=request.build_absolute_uri(),
                error=repr(exception),
                # 堆栈格式化
                tb=traceback.format_exc()
            )

            logger.warning(message)

            # send dingtalk message
            dingtalk.send(message)

            # capture exception to sentry
            capture_exception(exception)

        return HttpResponse("Error processing the request, please contact the system administrator.", status=500)
