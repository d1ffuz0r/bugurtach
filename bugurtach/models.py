# -*- coding: utf-8 -*-
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.db import models


class CustomUser(models.Model):

    """
    Custom user profile

    @param user: related with User model
    @param bugurts: All bugurts for user. Related with Bugurt model
    @param likes: All likes for user. Related with Like model
    @param info: Custom info for user
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
    """
    Tag

    Keyword arguments:
    @param title: name for tag
    """
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = u"Тег"
        verbose_name_plural = u"Теги"

    @classmethod
    def all(cls):
        """
        Return all tags

        @param cls:
        @return queryset:
        """
        return cls.objects.all()

    def get_absolute_url(self):
        """
        Absolute url

        @return unicode: link for tag
        """
        return u"/tags/%s/" % self.title

    def __unicode__(self):
        return self.title


class Proof(models.Model):
    """
    Proof

    @param link: url for proof
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
        """
        Return bugurt for name

        @param name: name for search bugurt
        @return queryset|bool:
        """
        result = self.get_query_set().filter(name=name)
        if result:
            return result[0]
        else:
            return None

    def get_by_author(self, username):
        """
        Absolute url

        @param username: name
        @return unicode: link for tag
        """
        result = self.get_query_set().filter(
            author=User.objects.get(username=username)
        )
        if result:
            return result
        else:
            return None

    def get_by_tag(self, tag):
        """
        Return bugurts for tag

        @param tag: name tag for search bugurt
        """
        tag_id = Tag.objects.get(title=tag)
        result = self.get_query_set().filter(tags=tag_id)
        return result

    def like(self, user, bugurt, type):
        """
        Like or Dislike bugurt

        @param user: id for user
        @param bugurt: id for bugurt
        @param type: like or dislike bugurt. aviable(0 or 1)
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
    """
    Bugurt model

    @param name: name bugurt. length=100
    @param text: text bugurt. length=10000
    @param date: date created bugurt. default(now)
    @param likes: likes bugurt. default(0)
    @param author: author bugurt. related with model User
    @param tags: tags bugurt. related with model Tag
    @param proofs: proofs bugurt. related with model Proof
    @param comments: commentaries bugurt. related with model Comments
    @param objects: manager BugurtManager
    @param manager: BugurtManager
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
        """
        Absolute url

        @return unicode: link for bugurt
        """
        return u"/bugurts/%s/" % self.name


class BugurtTags(models.Model):
    """
    Tags for Bugurt. Model for related Bugurt and Tag

    @param bugurt: bugurt object
    @param tag: tag object
    """
    bugurt = models.ForeignKey(Bugurt)
    tag = models.ForeignKey(Tag)

    class Meta:
        verbose_name = u"Тег бугурта"
        verbose_name_plural = u"Теги бугуртов"

    def __unicode__(self):
        return self.tag.title


class BugurtProofs(models.Model):
    """
    Proofs for Bugurt. Model for related Bugurt and Proof

    @param bugurt: bugurt object
    @param proof: proof object
    """
    bugurt = models.ForeignKey(Bugurt)
    proof = models.ForeignKey(Proof)

    class Meta:
        verbose_name = u"Пруф бугурта"
        verbose_name_plural = u"Пруфы бугуртов"

    def __unicode__(self):
        return self.proof.link


class Like(models.Model):
    """
    Like

    @param user_id: user object
    @param bugurt_id: bugurt object
    @param type: 1(like) or 0(dislike)
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
    """
    Commentaries

    @param author: user object
    @param bugurt: bugurt object
    @param date: date create commentaries. default(now)
    @param text: text commentaries
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
