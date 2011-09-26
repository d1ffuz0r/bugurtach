# -*- coding: utf-8 -*-
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.db import models
from django.http import Http404

class CustomUser(models.Model):
    user = models.OneToOneField(User, unique=True)
    bugurts = models.ManyToManyField('Bugurt', blank=True)
    likes = models.ManyToManyField('Like', blank=True)
    info = models.TextField(max_length=1000, blank=True)

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

class Tag(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = u'Тег'
        verbose_name_plural = u'Теги'

    @classmethod
    def all(cls):
        return cls.objects.all()

    def __unicode__(self):
        return self.title

class Proof(models.Model):
    link = models.CharField(max_length=500)

    class Meta:
        verbose_name = u'Пруф'
        verbose_name_plural = u'Пруфы'

    def __unicode__(self):
        return self.link

class Bugurt(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField(max_length=10000)
    date = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(max_length=10, blank=True, default=0)
    author = models.ForeignKey(User)
    tags = models.ManyToManyField(Tag, through='BugurtTags', blank=True)
    proofs = models.ManyToManyField(Proof, through='BugurtProofs')
    comments = models.ManyToManyField('Comments', blank=True, related_name='bugurtcomments')

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
            Like.objects.create(bugurt_id=Bugurt.objects.get(id=bugurt), user_id=user, type=type)
            bugu = cls.objects.get(id=bugurt)
            if type == 'like':
                bugu.likes += 1
                bugu.save()
            if type == 'dislike':
                bugu.likes -= 1
                bugu.save()
        return bugu.likes

class BugurtTags(models.Model):
    bugurt = models.ForeignKey(Bugurt)
    tag = models.ForeignKey(Tag)

    class Meta:
        verbose_name = u'Тег бугурта'
        verbose_name_plural = u'Теги бугуртов'

    def __unicode__(self):
        return '%s : %s' %(self.bugurt, self.tag)

class BugurtProofs(models.Model):
    bugurt = models.ForeignKey(Bugurt)
    proof = models.ForeignKey(Proof)

    class Meta:
        verbose_name = u'Пруф бугурта'
        verbose_name_plural = u'Пруфы бугуртов'

    def __unicode__(self):
        return '%s : %s' %(self.bugurt, self.proof)

class Like(models.Model):
    user_id = models.ForeignKey(User)
    bugurt_id = models.ForeignKey(Bugurt)
    type = models.CharField(max_length=10, blank=False)

    class Meta:
        verbose_name = u'Голос'
        verbose_name_plural = u'Голоса'

    def __unicode__(self):
        return '%s : %s' % (self.user_id.username, self.bugurt_id.name)

class Comments(models.Model):
    author  = models.ForeignKey(User)
    bugurt = models.ForeignKey(Bugurt, related_name='bugurtcomments')
    date = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=1000)

    class Meta:
        verbose_name = u'Комментарий'
        verbose_name_plural = u'Комментарии'

    def __unicode__(self):
        return '%s : %s...' % (self.author, self.text)