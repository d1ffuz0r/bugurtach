# -*- coding: utf-8 -*-
from datetime import datetime
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from bugurtach.models import Bugurt, Comments

class TestAjaxForms(TestCase):

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
        self.comment = Comments.objects.create(author=self.user,
                                               bugurt=self.bugurt,
                                               text="test")

    def test_reply(self):
        request = self.client.get("/ajax/reply/")
        self.assertContains(request, text="test")

    def test_like(self):
        self.client.post("/login/", {"username": "root1", "password": "root"})
        request = self.client.post("/ajax/like/", {"bugurt_id": self.bugurt.id,
                                                   "type": "like"},
                                                   **{'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'})
        self.assertContains(request, text='{"message": "\u041e\u0445\u0443\u0435\u043d\u043d\u043e!", "post": "1", "likes": 1}')
        request1 = self.client.post("/ajax/like/", {"bugurt_id": self.bugurt.id,
                                                    "type": "like"},
                                                    **{'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'})
        self.assertContains(request1, text='{"message": "\u0412\u044b \u0443\u0436\u0435 \u0433\u043e\u043b\u043e\u0441\u043e\u0432\u0430\u043b\u0438 \u0437\u0430 \u044d\u0442\u043e\u0442 \u0431\u0443\u0433\u0443\u0440\u0442"}')

    def test_dislike(self):
        self.client.post("/login/", {"username": "root1", "password": "root"})
        request = self.client.post("/ajax/like/", {"bugurt_id": self.bugurt.id,
                                                  "type": "dislike"},
                                                  **{'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'})
        self.assertContains(request, text='{"message": "\u0425\u0443\u0438\u0442\u0430", "post": "1", "likes": -1}')
        request1 = self.client.post("/ajax/like/", {"bugurt_id": self.bugurt.id,
                                                    "type": "dislike"},
                                                    **{'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'})
        self.assertContains(request1, text='{"message": "\u0412\u044b \u0443\u0436\u0435 \u0433\u043e\u043b\u043e\u0441\u043e\u0432\u0430\u043b\u0438 \u0437\u0430 \u044d\u0442\u043e\u0442 \u0431\u0443\u0433\u0443\u0440\u0442"}')

    def test_add_comment(self):
        self.client.post("/login/", {"username": "root1", "password": "root"})
        request = self.client.post("/ajax/add_comment/", {"bugurt": 1, "text": "test1"},
                                **{'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'})
        request1 = self.client.post("/ajax/add_comment/", {"bugurt": 1, "text": "test1"},
                                **{'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'})
        request2 = self.client.post("/ajax/add_comment/", {"bugurt": 1, "text": ""},
                                **{'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'})
        self.assertContains(request, text='{"comment": {"date": "%s", "text": "test1", "id": 2, "author": "root1"}}' % datetime.now().strftime("%d.%m.%y, %H:%M"))
        self.assertContains(request1, text='{"message": "\u0423\u0436\u0435 \u0435\u0441\u0442\u044c"}')
        self.assertContains(request2, text='{"message": "\u041d\u0430\u043f\u0438\u0448\u0438 \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435"}')

    def test_add_tag(self):
        self.client.post("/login/", {"username": "root1", "password": "root"})
        request = self.client.post("/ajax/add_tag/", {"bugurt": 1, "tag": "tag1"},
                                **{'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'})
        request1 = self.client.post("/ajax/add_tag/", {"bugurt": 1, "tag": "tag1"},
                                **{'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'})
        request2 = self.client.post("/ajax/add_tag/", {"bugurt": 1, "tag": ""},
                                **{'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'})
        self.assertContains(request, text='{"tag": "tag1", "id": 1}')
        self.assertContains(request1, text='{"message": "\u0423\u0436\u0435 \u0435\u0441\u0442\u044c"}')
        self.assertContains(request2, text='{"message": "\u0412\u0432\u0435\u0434\u0438 \u0442\u0435\u0433"}')
        self.client.logout()
        self.client.post("/login/", {"username": "d1ffuz0r", "password": "root"})
        request3 = self.client.post("/ajax/add_tag/", {"bugurt": 1, "tag": "tag1"},
                                    **{'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'})
        self.assertContains(request3, text='{"message": "\u0427\u0438\u0442\u0430\u043a \u0451\u043f\u0442\u0430?"}')

    def test_delete_tag(self):
        self.client.post("/login/", {"username": "root1", "password": "root"})
        self.client.post("/ajax/add_tag/",{"bugurt": 1, "tag": "tag1"},
                                **{'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'})
        request = self.client.post("/ajax/delete_tag/",{"bugurt": 1, "tag": "tag1"},
                                           **{'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'})
        self.assertContains(request, text="null")

    def test_add_proof(self):
        self.client.post("/login/", {"username": "root1", "password": "root"})
        request = self.client.post("/ajax/add_proof/", {"bugurt": 1, "proof": "proof1"},
                                **{'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'})
        request1 = self.client.post("/ajax/add_proof/", {"bugurt": 1, "proof": "proof1"},
                                **{'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'})
        request2 = self.client.post("/ajax/add_proof/",{"bugurt": 1, "proof": ""},
                                **{'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'})
        self.assertContains(request, text='{"id": 1, "proof": "proof1"}')
        self.assertContains(request1, text='{"message": "\u0423\u0436\u0435 \u0435\u0441\u0442\u044c"}')
        self.assertContains(request2, text='{"message": "\u0412\u0432\u0435\u0434\u0438 \u043f\u0440\u0443\u0444"}')
        self.client.logout()
        self.client.post("/login/", {"username": "d1ffuz0r", "password": "root"})
        request3 = self.client.post("/ajax/add_proof/",{"bugurt": 1, "proof": "proof1"},
                                    **{'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'})
        self.assertContains(request3, text='{"message": "\u0427\u0438\u0442\u0430\u043a \u0451\u043f\u0442\u0430?"}')


    def test_delete_proof(self):
        self.client.post("/login/", {"username": "root1", "password": "root"})
        self.client.post("/ajax/delete_proof/",{"bugurt": 1, "proof": "proof1"},
                                **{'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'})
        request = self.client.post("/ajax/delete_proof/",{"bugurt": 1, "proof": "proof1"},
                                   **{'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'})
        self.assertContains(request, text="null")

    def test_autocomplite(self):
        self.client.post("/login/", {"username": "root1", "password": "root"})
        self.client.post("/ajax/add_tag/",{"bugurt": 1, "tag": "tag1"},
                                        **{'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'})
        request = self.client.post("/ajax/autocomplite/", {"text": "tag1"}, **{'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'})
        self.assertContains(request, text="<li>tag1</li>")

    def test_decorator_ajax(self):
        request = self.client.post("/ajax/add_tag/",{"bugurt": 1, "tag": "tag1"},
                                                **{'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'})
        request1 = self.client.post("/ajax/add_tag/",{"bugurt": 1, "tag": "tag1"})
        self.assertContains(request, text='{"message": "\u0417\u0430\u043b\u043e\u0433\u0438\u043d\u044c\u0441\u044f \u0441\u0443\u0447\u0435\u0447\u043a\u0430"}')
        self.assertContains(request1, text='{"message": "WOK!"}')

    def doCleanups(self):
        self.bugurt.delete()