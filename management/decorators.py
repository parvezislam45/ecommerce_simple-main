from django.http import Http404
from django.shortcuts import render
from functools import wraps

def superuser_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            # Raise a 404 error for non-superusers
            raise Http404("Page not found")
    return _wrapped_view