# -*- coding: utf-8 -*-

from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from bugurtach.models import Bugurt, User, Tag


class UserFeed(Feed):
    title = u"Bugurtach.tk. Cамые сочные бугурты"
    link = u"/bugurts/"

    def get_object(self, request, name):
        return get_object_or_404(User, username=name)

    def item_link(self, obj):
        return obj.get_absolute_url()

    def item_title(self, obj):
        return obj.name

    def item_description(self, obj):
            return obj.text

    def description(self, obj):
        return u"Бугурты от %s" % obj.username

    def items(self, obj):
        return Bugurt.objects.filter(author=obj).all()[:10]


class TagFeed(Feed):
    title = u"Bugurtach.tk. Cамые сочные бугурты"
    link = u"/tags/"

    def get_object(self, request, name):
        return get_object_or_404(Tag, title=name)

    def item_title(self, obj):
        return obj.name

    def item_link(self, obj):
        return obj.get_absolute_url()

    def item_description(self, obj):
        return obj.text

    def description(self, obj):
        return u"Бугурты по тегу %s" % obj.title

    def items(self, obj):
        return Bugurt.objects.filter(tags=obj).all()[:10]
