# -*- coding: utf-8 -*-
from functools import wraps
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
#from django.views.decorators.cache import cache_control
from django.utils import simplejson

def render_to(template):
    """
    decorator for rendering views to template
    """
    def renderer(func):
        @wraps(func)
        #@cache_control(must_revalidate=True, max_age=3600)
        def wrapper(request, *args, **kwargs):
            output = func(request, *args, **kwargs)
            if isinstance(output, (list, tuple)):
                return render_to_response(output[1], output[0], context_instance=RequestContext(request))
            elif isinstance(output, dict):
                return render_to_response(template, output, context_instance=RequestContext(request))
            return output
        return wrapper
    return renderer

def render_json(func):
    """
    decorator for rendering data as json
    """
    def wrap(request, *args, **kwargs):
        response = None
        try:
            response = func(request, *args, **kwargs)
            assert isinstance(response, dict)
        except ValueError:
            pass
        return HttpResponse(simplejson.dumps(response), mimetype="application/json")
    return wrap

def check_ajax(func):
    """
    decorator for check on login and ajax method
    """
    def wrap(request, *args, **kwargs):
        user = request.user
        if request.is_ajax():
            if user.is_authenticated():
                return func(request, *args, **kwargs)
            else:
                res = func.result={"message":"Залогинься сучечка"}
                return res
        else:
            res = func.result={"message":"WOK!"}
            return res
    return wrap