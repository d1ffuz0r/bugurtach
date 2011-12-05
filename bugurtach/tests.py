# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from bugurtach.models import Tag, Proof, CustomUser, Bugurt,\
    BugurtTags, Like, Comments, BugurtProofs
from ajax.tests import TestAjaxForms


class TestModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="root1",
                                             email="test@email.com",
                                             password="root")
        self.user2 = User.objects.create_user(username="root2",
                                              email="test@email.com",
                                              password="root")
        self.cuser = CustomUser.objects.filter(user__username="root1").get()
        self.tag = Tag.objects.create(title="test")
        self.proof = Proof.objects.create(link="google.com")
        self.bugurt = Bugurt.objects.create(name="test",
                                        text="testtest",
                                        author=self.user)
        self.bugurttag = BugurtTags.objects.create(
            bugurt=self.bugurt,
            tag=self.tag
        )
        self.bugurtproof = BugurtProofs.objects.create(
            bugurt=self.bugurt,
            proof=self.proof
        )
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
        self.assertTrue(Bugurt.manager.like(self.user, self.bugurt.id, "1"))
        self.assertFalse(Bugurt.manager.like(self.user, self.bugurt.id, "1"))

    def test_bugurt_dislike(self):
        self.assertTrue(Bugurt.manager.like(self.user, self.bugurt.id, "0"))
        self.assertFalse(Bugurt.manager.like(self.user, self.bugurt.id, "0"))

    def test_bugurttags(self):
        self.assertEqual(self.bugurttag.__unicode__(), "test")

    def test_bugurtproofs(self):
        self.assertEqual(self.bugurtproof.__unicode__(), "google.com")

    def test_like(self):
        self.assertTrue(Bugurt.manager.like(self.user, self.bugurt.id, "1"))
        self.assertEqual(
            Like.objects.get(bugurt_id=self.bugurt.id).__unicode__(),
            "root1 : test"
        )

    def test_dislike(self):
        self.assertTrue(Bugurt.manager.like(self.user, self.bugurt.id, "0"))
        self.assertNotEqual(
            Like.objects.get(bugurt_id=self.bugurt.id).__unicode__(),
            "root1 : test2"
        )

    def test_comment(self):
        self.assertEqual(self.comment.__unicode__(), "root1 : test...")

    def test_comment_latest(self):
        self.assertEqual(
            self.comment.latest_comments()[0].author.username,
            "root1"
        )

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
        self.user1 = User.objects.create_user(username="d1ffuz0r",
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
        request = self.client.post("/registration/",
                {"username": "roo",
                 "password1": "roo",
                 "password2": "roo"}
        )
        self.assertContains(request, text="", status_code=302)

    def test_register_false(self):
        request = self.client.post("/registration/",
                {"username": "roo",
                 "password1": "roo",
                 "password2": "roo1"}
        )
        self.assertContains(request, text="<!DOCTYPE html>")

    def test_add_bugurt(self):
        self.client.post("/login/", {"username": "root1", "password": "root"})
        request = self.client.get("/bugurts/add/")
        self.assertContains(request, text="author")

    def test_delete_bugurt_true(self):
        self.client.post("/login/", {"username": "root1", "password": "root"})
        request = self.client.get("/bugurts/test/delete/")
        self.assertContains(request, text="", status_code=302)

    def test_delete_bugurt_false(self):
        self.client.post("/login/", {"username": "d1ffuz0r",
                                     "password": "root"})
        request = self.client.get("/bugurts/test/delete/")
        self.assertRedirects(request, expected_url="/")

    def test_add_bugurt_true(self):
        self.client.post("/login/", {"username": "root1", "password": "root"})
        request = self.client.post("/bugurts/add/",
                {"text": "test",
                 "name": "test",
                 "author": 1,
                 "tags": "first, two, three",
                 "proofs": "googlem, yandes, rambler"}
        )
        self.assertRedirects(request, expected_url="/user/root1/")

    def test_add_bugurt_tags_fail(self):
        self.client.post("/login/", {"username": "root1", "password": "root"})
        request = self.client.post("/bugurts/add/",
                {"text": "test",
                 "name": "test",
                 "author": 1,
                 "tags": "",
                 "proofs": "googlem, yandes, rambler"}
        )
        self.assertContains(request, text="Введи тег(и)")

    def test_add_bugurt_tags_fail_whitespaces(self):
        self.client.post("/login/", {"username": "root1", "password": "root"})
        request = self.client.post("/bugurts/add/", {"text": "test",
                                                    "name": "test",
                                                    "author": 1,
                                                    "tags": "  ,  ",
                                                    "proofs": ", "})
        self.assertContains(request, text="Введи тег(и)")

    def test_add_bugurt_proofs_fail(self):
        self.client.post("/login/", {"username": "root1", "password": "root"})
        request = self.client.post("/bugurts/add/",
                {"text": "test",
                 "name": "test",
                 "author": 1,
                 "tags": "first, two, three",
                 "proofs": ""}
        )
        self.assertContains(request, text="Введи пруф(ы)")

    def test_edit_bugurt(self):
        self.client.post("/login/", {"username": "root1", "password": "root"})
        request = self.client.get("/bugurts/test/edit/")
        self.assertContains(request, text="text")

    def test_edit_bugurt_true(self):
        self.client.post("/login/", {"username": "root1", "password": "root"})
        request = self.client.post("/bugurts/test/edit/",
                {"name": "text",
                 "text": "text"}
        )
        self.assertRedirects(request, expected_url="/bugurts/text/")

    def test_edit_bugurt_false(self):
        self.client.post("/login/",
                {"username": "d1ffuz0r",
                 "password": "root"}
        )
        request = self.client.get("/bugurts/test/edit/")
        self.assertRedirects(request, expected_url="/bugurts/test/")

    def test_all_bugurts(self):
        request = self.client.get("/bugurts/")
        self.assertContains(request, text="<!DOCTYPE html>")

    def test_top_bugurts(self):
        request = self.client.get("/bugurts/top/")
        self.assertContains(request, text="<!DOCTYPE html>")

    def test_view_bugurt(self):
        request = self.client.get("/bugurts/test/")
        self.assertContains(request, text="test")

    def test_view_bugurt_none(self):
        request = self.client.get("/bugurts/test1/")
        self.assertContains(request, text="Not bugurt")

    def test_view_user(self):
        request = self.client.get("/user/root1/")
        self.assertContains(request, text="<!DOCTYPE html>")

    def test_view_user_none(self):
        request = self.client.get("/user/d1ffuz0r/")
        self.assertContains(request, text="Not bugurts")

    def test_user_login_true(self):
        request = self.client.post("/login/",
                {"username": "root1",
                 "password": "root"}
        )
        self.assertContains(request, text="", status_code=302)

    def test_user_settings(self):
        self.client.post("/login/",
                {"username": "root1",
                 "password": "root"}
        )
        request = self.client.get("/settings/")
        self.assertContains(request, text="Сменить пароль")

    def test_user_settings_true(self):
        self.client.post("/login/", {"username": "root1", "password": "root"})
        request1 = self.client.post("/settings/", {"old_password": "root",
                                                  "new_password1": "roo",
                                                  "new_password2": "roo"})
        self.assertContains(request1, text="Сохранено")

    def test_user_settings_false(self):
        self.client.post("/login/", {"username": "root1", "password": "root"})
        request1 = self.client.post("/settings/", {"old_password": "root",
                                                  "new_password1": "roo",
                                                  "new_password2": ""})
        self.assertContains(request1, text="This field is required.")

    def test_user_logout(self):
        request = self.client.get("/logout/")
        self.assertContains(request, text="", status_code=302)

    def test_user_login_false(self):
        request = self.client.post("/login/",
                {"username": "root1",
                 "password": "root1"}
        )
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
