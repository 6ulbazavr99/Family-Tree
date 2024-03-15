from django.utils.deprecation import MiddlewareMixin
from django.http import Http404
from django.shortcuts import render


class Custom404Middleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if isinstance(exception, Http404):
            return render(request, 'custom_404/custom_404.html', status=404)
        return None
