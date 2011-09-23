# -*- coding: utf-8 -*-
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.db import models
from django.http import Http404

class CustomUser(models.Model):
    user = models.OneToOneField(User, unique=True)
    bugurts = models.ManyToManyField('Bugurt', blank=True)
    likes = models.ManyToManyField('Like', blank=True)
    
    class Meta:
        verbose_name = u'Аккаунт'
        verbose_name_plural = u'Аккаунты'

    def get_absolute_url(self):
        return u'/user/%s/' % self.user

    def __unicode__(self):
        return self.user.username

def create_profile(**kwargs):
    user = kwargs['instance']
    if kwargs["created"]:
        profile = CustomUser(user=user)
        profile.save()

post_save.connect(create_profile, sender=User, dispatch_uid="users-profilecreation-signal")

class Bugurt(models.Model):
    id = models.IntegerField(auto_created=True, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    text = models.TextField(max_length=10000)
    date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(CustomUser)
    likes = models.IntegerField(max_length=10, blank=True, default=0)#models.ManyToManyField('Like', blank=True)
    tags = models.ManyToManyField('Tag', blank=True, through='BugurtTags')

    class Meta:
        verbose_name = u'Бугурт'
        verbose_name_plural = u'Бугурты'
        ordering = ('-date',)

    @classmethod
    def get_by_name(cls, name):
        result = cls.objects.filter(name__contains=name)
        if result:
            return result[0]
        else:
            raise Http404

    def get_absolute_url(self):
        return u'/bugurts/%s/' % self.name
    
    def __unicode__(self):
        return self.name

    @classmethod
    def get_by_author(cls, username):
        result = cls.objects.filter(author=User.objects.get(username=username))
        if result:
            return result
        else:
            return Http404

    @classmethod
    def get_by_tag(cls, tag):
        tag_id = Tag.objects.get(title=tag)
        result = cls.objects.filter(tags=tag_id)
        return result

    @classmethod
    def like(cls, user, bugurt, type):
        if Like.objects.filter(user_id=user).filter(bugurt_id=bugurt):
            return False
        else:
            Like.objects.create(bugurt_id=Bugurt.objects.get(id=bugurt), user_id=user)
            bugu = cls.objects.get(id=bugurt)
            if type == 'like':
                bugu.likes += 1
                bugu.save()
            if type == 'dislike':
                bugu.likes -= 1
                bugu.save()
        return True
    
class Like(models.Model):
    user_id = models.ForeignKey(User)
    bugurt_id = models.ForeignKey(Bugurt)

    class Meta:
        verbose_name = u'Голос'
        verbose_name_plural = u'Голоса'

    #def __unicode__(self):
    #    return self.user_id

class Tag(models.Model):
    title = models.CharField(max_length=100)
    bugurts = models.ManyToManyField(Bugurt, through='BugurtTags')

    class Meta:
        verbose_name = u'Тег'
        verbose_name_plural = u'Теги'

    @classmethod
    def all(cls):
        return cls.objects.all()

    @classmethod
    def create(cls, name):
        return cls.objects.create(name).save()

    def __unicode__(self):
        return self.title

class Proof(models.Model):
    pass

class BugurtTags(models.Model):
    id_bugurt = models.ForeignKey(Bugurt)
    id_tag = models.ForeignKey(Tag)