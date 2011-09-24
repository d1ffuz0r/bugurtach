from django import template
from bugurtach.models import Bugurt
register = template.Library()

@register.simple_tag(takes_context=True)
def latest_bugurt(context, user=None):
    if user:
        bugurts = Bugurt.get_by_author(user).order_by('-id')[:10]
    else:
        bugurts = Bugurt.objects.order_by('-id').all()[:10]
    context['latest_bugurts'] = bugurts
    return ''
