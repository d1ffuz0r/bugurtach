# -*- coding: utf-8 -*-
from decorators import render_to
from django.db.models import Max
from models import Bugurt

@render_to('home.html')
def homepage(request):
    bugurts = Bugurt.objects.all()
    comments = [{'title':'text static comment', 'url': '/bugurts/1#1'}]
    top = bugurts.all().aggregate(Max('likes'))
    return {'title': 'homepage',
            'bugurts': bugurts,
            'latest_bugurts': bugurts.order_by('-date')[:10],
            'latest_comments': comments,
            'top_bugurt': top}

@render_to('settings.html')
def user_settings(request):
    return {'test': 'static'}