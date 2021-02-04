from django.http import HttpResponse
from django.shortcuts import redirect

def is_unauthenticated(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper


def is_allowed(allowed_groups=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            
            if group in allowed_groups:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to access this page!')
        
        return wrapper
    return decorator
