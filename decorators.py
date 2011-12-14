# -*- coding: utf-8 -*-
from functools import wraps
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.simplejson import dumps
#from django.views.decorators.cache import cache_control


def render_to(template):
    """
    Decorator for rendering views to template

    @param template:
    @return page:
    """

    def renderer(func):
        @wraps(func)
        #@cache_control(must_revalidate=True, max_age=3600)
        def wrapper(request, *args, **kwargs):
            output = func(request, *args, **kwargs)
            if isinstance(output, (list, tuple)):
                return render_to_response(output[1],
                    output[0],
                    context_instance=RequestContext(request))
            elif isinstance(output, dict):
                return render_to_response(template,
                    output,
                    context_instance=RequestContext(request))
            return output
        return wrapper
    return renderer


def render_json(func):
    """
    Decorator for rendering data as json

    @param func:
    @return json:
    """
    def wrap(request, *args, **kwargs):
        response = None
        try:
            response = func(request, *args, **kwargs)
            assert isinstance(response, dict)
        except ValueError:
            pass
        return HttpResponse(dumps(response), mimetype="application/json")
    return wrap


def check_ajax(func):
    """
    Decorator for check on login and ajax method

    @param func:
    @return:
    """
    def wrap(request, *args, **kwargs):
        if request.is_ajax():
            if request.user.is_authenticated():
                return func(request, *args, **kwargs)
            else:
                return {"message": "Залогинься сучечка"}
        else:
            return {"message": "WOK!"}
    return wrap
