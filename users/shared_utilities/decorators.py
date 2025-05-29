from django.http import HttpResponseForbidden
from functools import wraps

def parent_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'parent'):
            return HttpResponseForbidden("Access denied: Parent account required.")
        return view_func(request, *args, **kwargs)
    return wrapper
