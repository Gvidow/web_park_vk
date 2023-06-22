from django.http import JsonResponse


class HttpResponseAjax(JsonResponse):
    def __init__(self, status="ok", **kwargs):
        kwargs["status"] = status
        super().__init__(kwargs)


class HttpResponseAjaxError(HttpResponseAjax):
    def __init__(self, code, message, **kwargs):
        super().__init__(status="error", code=code, message=message, **kwargs)


def login_required_ajax(handler):

    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseAjaxError(code="no_auth", message="login required")

        return handler(request, *args, **kwargs)
    return wrap
