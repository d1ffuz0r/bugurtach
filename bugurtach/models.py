# -*- coding: utf-8 -*-
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.db import models


class CustomUser(models.Model):
    """Custom user profile

    Keyword arguments:
    user -- related with User model
    bugurts -- All bugurts for user. Related with Bugurt model
    likes -- All likes for user. Related with Like model
    info -- Custom info for user

    """
    user = models.OneToOneField(User, unique=True)
    bugurts = models.ManyToManyField("Bugurt", blank=True)
    likes = models.ManyToManyField("Like", blank=True)
    info = models.TextField(max_length=1000, blank=True)

    class Meta:
        verbose_name = u"Аккаунт"
        verbose_name_plural = u"Аккаунты"

    def get_absolute_url(self):
        return u"/user/%s/" % self.user

    def __unicode__(self):
        return self.user.username


def create_profile(**kwargs):
    """Create User with create CustomUser"""
    user = kwargs["instance"]
    if kwargs["created"]:
        profile = CustomUser(user=user)
        profile.save()

post_save.connect(create_profile,
                  sender=User,
                  dispatch_uid="users-profilecreation-signal")


class Tag(models.Model):
    """Tag

    Keyword arguments:
    title -- name for tag

    """
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = u"Тег"
        verbose_name_plural = u"Теги"

    @classmethod
    def all(cls):
        """Return all tags"""
        return cls.objects.all()

    def get_absolute_url(self):
        return u"/tags/%s/" % self.title

    def __unicode__(self):
        return self.title


class Proof(models.Model):
    """Proof

    Keyword arguments:
    link -- url for proof

    """
    link = models.CharField(max_length=500)

    class Meta:
        verbose_name = u"Пруф"
        verbose_name_plural = u"Пруфы"

    def __unicode__(self):
        return self.link


class BugurtManager(models.Manager):
    """Manager for Bugurt model management"""
    def all(self):
        """Return all bugurts"""
        return self.get_query_set().order_by("-date")

    def get_by_name(self, name):
        """Return bugurt for name

        Keyword arguments:
        name -- name for search bugurt

        """
        result = self.get_query_set().filter(name=name)
        if result:
            return result[0]
        else:
            return None

    def get_by_author(self, username):
        """Return bugurt for author

        Keyword arguments:
        username -- author for search bugurt

        """
        result = self.get_query_set().filter(
            author=User.objects.get(username=username)
        )
        if result:
            return result
        else:
            return None

    def get_by_tag(self, tag):
        """Return bugurts for tag

        Keyword arguments:
        tag -- name tag for search bugurt

        """
        tag_id = Tag.objects.get(title=tag)
        result = self.get_query_set().filter(tags=tag_id)
        return result

    def like(self, user, bugurt, type):
        """Like or Dislike bugurt

        Keyword arguments:
        user -- id for user
        bugurt -- id for bugurt
        type -- like or dislike bugurt. aviable(0 or 1)

        """
        if Like.objects.filter(user_id=user).filter(bugurt_id=bugurt):
            return False
        else:
            Like.objects.create(bugurt_id=Bugurt.objects.get(id=bugurt),
                                user_id=user,
                                type=type)
            bugurt_obj = self.get_query_set().get(id=bugurt)
            if type == "1":
                bugurt_obj.likes += 1
                bugurt_obj.save()
            if type == "0":
                bugurt_obj.likes -= 1
                bugurt_obj.save()
        return bugurt_obj.likes

    def top(self):
        """Return top10 bugurts"""
        return self.get_query_set().order_by("-likes", "-comments")[:10]

    def latest(self):
        """Return latest 10 bugurts"""
        return self.get_query_set().order_by("-id")[:10]


class Bugurt(models.Model):
    """Bugurt model

    Keyword arguments:
    name -- name bugurt. length=100
    text -- text bugurt. length=10000
    date -- date created bugurt. default(now)
    likes -- likes bugurt. default(0)
    author -- author bugurt. related with model User
    tags -- tags bugurt. related with model Tag
    proofs -- proofs bugurt. related with model Proof
    comments -- commentaries bugurt. related with model Comments
    objects -- manager BugurtManager
    manager -- BugurtManager

    """
    name = models.CharField(max_length=100, verbose_name=u"Заголовок")
    text = models.TextField(max_length=10000, verbose_name=u"Текст")
    date = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(max_length=10, blank=True, default=0)
    author = models.ForeignKey(User)
    tags = models.ManyToManyField(Tag, through="BugurtTags", blank=True)
    proofs = models.ManyToManyField(Proof, through="BugurtProofs")
    comments = models.ManyToManyField("Comments",
        related_name="buburtcomments",
        blank=True)
    objects = models.Manager()
    manager = BugurtManager()

    class Meta:
        verbose_name = u"Бугурт"
        verbose_name_plural = u"Бугурты"
        ordering = ("-date",)
        get_latest_by = "date"

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return u"/bugurts/%s/" % self.name


class BugurtTags(models.Model):
    """Tags for Bugurt. Model for related Bugurt and Tag

    Keyword arguments:
    bugurt -- bugurt object
    tag -- tag object

    """
    bugurt = models.ForeignKey(Bugurt)
    tag = models.ForeignKey(Tag)

    class Meta:
        verbose_name = u"Тег бугурта"
        verbose_name_plural = u"Теги бугуртов"

    def __unicode__(self):
        return self.tag.title


class BugurtProofs(models.Model):
    """Proofs for Bugurt. Model for related Bugurt and Proof

    Keyword arguments:
    bugurt -- bugurt object
    proof -- proof object

    """
    bugurt = models.ForeignKey(Bugurt)
    proof = models.ForeignKey(Proof)

    class Meta:
        verbose_name = u"Пруф бугурта"
        verbose_name_plural = u"Пруфы бугуртов"

    def __unicode__(self):
        return self.proof.link


class Like(models.Model):
    """Like

    Keyword arguments:
    user_id -- user object
    bugurt_id -- bugurt object
    type -- 1(like) or 0(dislike)

    """
    CHOISES = (("1", "like"),
               ("0", "dislike"))
    user_id = models.ForeignKey(User)
    bugurt_id = models.ForeignKey(Bugurt)
    type = models.CharField(max_length=20, choices=CHOISES)

    class Meta:
        verbose_name = u"Голос"
        verbose_name_plural = u"Голоса"

    def __unicode__(self):
        return "%s : %s" % (self.user_id.username, self.bugurt_id.name)


class Comments(models.Model):
    """Commentaries

    Keyword arguments:
    author -- user object
    bugurt -- bugurt object
    date -- date create commentaries. default(now)
    text -- text commentaries

    """
    author = models.ForeignKey(User)
    bugurt = models.ForeignKey(Bugurt, related_name="bugurtcomments")
    date = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=1000)

    class Meta:
        verbose_name = u"Комментарий"
        verbose_name_plural = u"Комментарии"

    def __unicode__(self):
        return "%s : %s..." % (self.author, self.text)

    @classmethod
    def latest_comments(cls):
        """Return latest 10 commentaries"""
        return cls.objects.order_by("-id")[:10]
