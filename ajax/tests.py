from bugurtach.models import Bugurt, Comments
from django.contrib.auth.models import User
from django.test.client import Client
from django.test import TestCase

class TestAjaxForms(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="root1",
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
        request = self.client.post("/ajax/like/",{"bugurt_id": self.bugurt.id,
                                                  "type": "dislike"},
                                                  **{'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'})
        self.assertContains(request, text='{"message": "\u0425\u0443\u0438\u0442\u0430", "post": "1", "likes": -1}')
        request1 = self.client.post("/ajax/like/",{"bugurt_id": self.bugurt.id,
                                                   "type": "dislike"},
                                                   **{'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'})
        self.assertContains(request1, text='{"message": "\u0412\u044b \u0443\u0436\u0435 \u0433\u043e\u043b\u043e\u0441\u043e\u0432\u0430\u043b\u0438 \u0437\u0430 \u044d\u0442\u043e\u0442 \u0431\u0443\u0433\u0443\u0440\u0442"}')

    def test_add_comment(self):
        pass

    def test_add_tag(self):
        pass

    def test_delete_tag(self):
        pass

    def test_add_proof(self):
        pass

    def test_delete_proof(self):
        pass

    def test_autocomplite(self):
        pass

    def doCleanups(self):
        self.bugurt.delete()