# -*- coding: utf-8 -*-
from django.test import TestCase
from bugurtach.models import Tag, Proof, CustomUser, Bugurt, BugurtTags, Like, Comments, BugurtProofs
from django.contrib.auth.models import User
from django.test.client import Client
from ajax.tests import TestAjaxForms

class TestModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="root1",
                                             email="test@email.com",
                                             password="root")
        self.user2 = User.objects.create_user(username="root2",
                                              email="test@email.com",
                                              password="root")
        self.cuser = CustomUser.objects.filter(user__username ="root1").get()
        self.tag = Tag.objects.create(title="test")
        self.proof = Proof.objects.create(link="google.com")
        self.bugurt = Bugurt.objects.create(name="test",
                                        text="testtest",
                                        author=self.user)
        self.bugurttag = BugurtTags.objects.create(bugurt=self.bugurt, tag=self.tag)
        self.bugurtproof = BugurtProofs.objects.create(bugurt=self.bugurt, proof=self.proof)
        self.comment = Comments.objects.create(author=self.user,
                                               bugurt=self.bugurt,
                                               text="test")

    def test_tag_equal(self):
        self.assertEqual(self.tag.__unicode__(), 'test')

    def test_tag_not_equal(self):
        self.assertNotEqual(self.tag.__unicode__(), 'test1')

    def test_tag_absolute_url(self):
        self.assertEqual(self.tag.get_absolute_url(), '/tags/test/')

    def test_tga_get_all(self):
        self.assertIn(self.tag, self.tag.all())

    def test_proof_equal(self):
        self.assertEqual(self.proof.__unicode__(), "google.com")

    def test_proof_not_equal(self):
        self.assertNotEqual(self.proof.__unicode__(), "ya.ru")

    def test_user_equal(self):
        self.assertEqual(self.user.username, "root1")

    def test_customuser_equal(self):
        self.assertEqual(self.cuser.__unicode__(), "root1")

    def test_customuser_absolute_url(self):
        self.assertEqual(self.cuser.get_absolute_url(), u"/user/root1/")

    class data(object):
        data = {"tags": "first, two, three",
                "proofs": "google, yandex, rambler",
                "name": "test",
                "text": "message"}

    def test_create_bugurt(self):
        self.assertIsNone(Bugurt.manager.create_bugurt(
            form=self.data,
            user=self.user
        ))

    def test_bugurt_equal(self):
        self.assertEqual(self.bugurt.__unicode__(), "test")

    def test_bugurt_not_equal(self):
        self.assertNotEqual(self.bugurt.__unicode__(), "test1")

    def test_bugurt_all(self):
        self.assertEqual(len(Bugurt.manager.all()), 1)

    def test_bugurt_by_name(self):
        self.assertEqual(Bugurt.manager.get_by_name("test").name, "test")

    def test_bugurt_by_name_error(self):
        self.assertFalse(Bugurt.manager.get_by_name("nosdfag"))

    def test_bugurt_by_author(self):
        self.assertEqual(Bugurt.manager.get_by_author("root1")[0].name, "test")

    def test_bugurt_by_author_error(self):
        self.assertFalse(Bugurt.manager.get_by_author("root2"))

    def test_bugurt_by_tag(self):
        self.assertEqual(Bugurt.manager.get_by_tag("test")[0].name, "test")

    def test_bugurt_top(self):
        self.assertEqual(Bugurt.manager.top()[0].name, "test")

    def test_bugurt_latest(self):
        self.assertEqual(Bugurt.manager.latest()[0].name, "test")

    def test_bugurt_absolute_url(self):
        self.assertEqual(self.bugurt.get_absolute_url(), u"/bugurts/test/")

    def test_bugurt_like(self):
        self.assertTrue(Bugurt.manager.like(self.user, self.bugurt.id ,"like"))
        self.assertFalse(Bugurt.manager.like(self.user, self.bugurt.id ,"like"))

    def test_bugurt_dislike(self):
        self.assertTrue(Bugurt.manager.like(self.user, self.bugurt.id ,"dislike"))
        self.assertFalse(Bugurt.manager.like(self.user, self.bugurt.id ,"dislike"))

    def test_bugurttags(self):
        self.assertEqual(self.bugurttag.__unicode__(), "test")

    def test_bugurtproofs(self):
        self.assertEqual(self.bugurtproof.__unicode__(), "google.com")

    def test_like(self):
        self.assertTrue(Bugurt.manager.like(self.user, self.bugurt.id ,"like"))
        self.assertEqual(Like.objects.get(bugurt_id=self.bugurt.id).__unicode__(), "root1 : test")

    def test_dislike(self):
        self.assertTrue(Bugurt.manager.like(self.user, self.bugurt.id ,"like"))
        self.assertNotEqual(Like.objects.get(bugurt_id=self.bugurt.id).__unicode__(), "root1 : test2")

    def test_comment(self):
        self.assertEqual(self.comment.__unicode__(), "root1 : test...")

    def test_comment_latest(self):
        self.assertEqual(self.comment.latest_comments()[0].author.username, "root1")

    def doCleanups(self):
        self.user.delete()
        self.user2.delete()
        self.cuser.delete()
        self.tag.delete()
        self.proof.delete()
        self.bugurt.delete()
        self.comment.delete()
        self.bugurttag.delete()
        self.bugurtproof.delete()

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="root1",
                                             email="test@email.com",
                                             password="root")
        self.bugurt = Bugurt.objects.create(name="test",
                                        text="testtest",
                                        author=self.user)
        self.tag = Tag.objects.create(title="test")

    def test_home(self):
        request = self.client.get("/")
        self.assertContains(request, text="<!DOCTYPE html>")

    def test_register_page(self):
        request = self.client.get("/registration/")
        self.assertContains(request, text="<!DOCTYPE html>")

    def test_register_true(self):
        request = self.client.post("/registration/", {"username": "roo", "password1": "roo", "password2": "roo"})
        self.assertContains(request, text="", status_code=302)

    def test_register_false(self):
        request = self.client.post("/registration/", {"username": "roo", "password1": "roo", "password2": "roo1"})
        self.assertContains(request, text="<!DOCTYPE html>")

    def test_delete_bugurt(self):
        self.client.post("/login/", {"username": "root1", "password": "root"})
        request = self.client.get("/bugurts/test/delete/")
        self.assertContains(request, text="", status_code=302)

    def test_all_bugurts(self):
        request = self.client.get("/bugurts/")
        self.assertContains(request, text="<!DOCTYPE html>")

    def test_view_not_bugurt(self):
        request = self.client.get("/bugurts/test/")
        self.assertContains(request, text="<!DOCTYPE html>")

    def test_view_user(self):
        request = self.client.get("/user/root1/")
        self.assertContains(request, text="<!DOCTYPE html>")

    def test_user_login_true(self):
        request = self.client.post("/login/", {"username": "root1", "password": "root"})
        self.assertContains(request, text="", status_code=302)

    def test_user_settings_true(self):
        self.client.post("/login/", {"username": "root1", "password": "root"})
        request = self.client.get("/settings/")
        self.assertContains(request, text="<!DOCTYPE html>")
        request1 = self.client.post("/settings/", {"old_password": "root1",
                                                  "new_password1": "roo",
                                                  "new_password2": "roo" })
        self.assertContains(request1, text="<!DOCTYPE html>")

    def test_user_logout(self):
        request = self.client.get("/logout/")
        self.assertContains(request, text="", status_code=302)

    def test_user_login_false(self):
        request = self.client.post("/login/", {"username": "root1", "password": "root1"})
        self.assertContains(request, text="<!DOCTYPE html>")

    def test_view_tags(self):
        request = self.client.get("/tags/")
        self.assertContains(request, text="<!DOCTYPE html>")

    def test_view_tag(self):
        request = self.client.get("/tags/test/")
        self.assertContains(request, text="<!DOCTYPE html>")

    def doCleanups(self):
        self.user.delete()
        self.tag.delete()
        self.bugurt.delete()

    TestAjaxForms