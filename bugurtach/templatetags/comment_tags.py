from django import template
from bugurtach.models import Comments
register = template.Library()

@register.simple_tag(takes_context=True)
def comments_bugurt(context, bugurt, right=None):
    if right:
        comments = Comments.objects.filter(bugurt=bugurt).order_by('date')[:5]
    else:
        comments = Comments.objects.filter(bugurt=bugurt).order_by('date')
    context['comments'] = comments
    return ''

@register.simple_tag(takes_context=True)
def latest_comments(context, user=None):
    if user:
        comments = Comments.objects.filter(author=user).order_by('date')[:5]
    else:
        comments = Comments.objects.order_by('date')[:10]
    context['latest_comments'] = comments
    return ''