from functools import wraps
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.cache import cache_control

def render_to(template):
    """
    decorator for rendering views to template
    """
    def renderer(func):
        @wraps(func)
        @cache_control(must_revalidate=True, max_age=3600)
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
            if isinstance(output, (list, tuple)):
                return render_to_response(output[1], output[0], context_instance=RequestContext(request))
            elif isinstance(output, dict):
                return render_to_response(template, output, context_instance=RequestContext(request))
            return output
        return wrapper
    return renderer
  