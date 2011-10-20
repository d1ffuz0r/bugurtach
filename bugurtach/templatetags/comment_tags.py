from django import template
from bugurtach.models import Comments
register = template.Library()

@register.simple_tag(takes_context=True)
def comments_bugurt(context, bugurt):
    comments = Comments.objects.filter(bugurt=bugurt).order_by("date")
    context["comments"] = comments
    return ""