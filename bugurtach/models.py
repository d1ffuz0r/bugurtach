# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class CustomUser(models.Model):
    user = models.OneToOneField(User, unique=True)
    bugurts = models.ManyToManyField('Bugurt')

    class Meta:
        verbose_name = u'Аккаунт'
        verbose_name_plural = u'Аккаунты'

    def __unicode__(self):
        return self.user.username

def create_profile(**kwargs):
    user = kwargs['instance']
    if kwargs["created"]:
        profile = CustomUser(user=user)
        profile.save()

post_save.connect(create_profile, sender=User)

class Bugurt(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField(max_length=10000)
    date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(CustomUser)
    rating = models.PositiveIntegerField(max_length=10)
    class Meta:
        verbose_name = u'Бугурт'
        verbose_name_plural = u'Бугурты'

    def __unicode__(self):
        return self.name