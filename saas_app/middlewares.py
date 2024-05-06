# saas_app/middlewares.py

from django.http import HttpResponseForbidden

class AdminDashboardMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/dashboard/':
            if not request.user.is_staff:
                return HttpResponseForbidden()
        response = self.get_response(request)
        return response
