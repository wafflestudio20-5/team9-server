from django import http


class HealthCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: http.HttpRequest):
        if request.path == "/ping":
            return http.HttpResponse("pong")
        response = self.get_response(request)
        return response
