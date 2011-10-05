from django.contrib.auth.models import User
from unittest import TestCase
from bugurtach.models import Tag, Proof, CustomUser, Bugurt, BugurtTags, Like, Comments, BugurtProofs

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

    def test_bugurt_equal(self):
        self.assertEqual(self.bugurt.__unicode__(), "test")

    def test_bugurt_not_equal(self):
        self.assertNotEqual(self.bugurt.__unicode__(), "test1")

    def test_bugurt_all(self):
        self.assertEqual(len(self.bugurt.all()), 1)

    def test_bugurt_by_name(self):
        self.assertEqual(self.bugurt.get_by_name("test")[0].name, "test")

    def test_bugurt_by_name_error(self):
        self.assertFalse(self.bugurt.get_by_name("nosdfag"))

    def test_bugurt_by_author(self):
        self.assertEqual(self.bugurt.get_by_author("root1")[0].name, "test")

    def test_bugurt_by_author_error(self):
        self.assertFalse(self.bugurt.get_by_author("root2"))

    def test_bugurt_by_tag(self):
        self.assertEqual(self.bugurt.get_by_tag("test")[0].name, "test")

    def test_bugurt_top(self):
        self.assertEqual(self.bugurt.top()[0].name, "test")

    def test_bugurt_latest(self):
        self.assertEqual(self.bugurt.latest()[0].name, "test")

    def test_bugurt_absolute_url(self):
        self.assertEqual(self.bugurt.get_absolute_url(), u"/bugurts/test/")

    def test_bugurt_like(self):
        self.assertTrue(self.bugurt.like(self.user, self.bugurt.id ,"like"))
        self.assertFalse(self.bugurt.like(self.user, self.bugurt.id ,"like"))

    def test_bugurt_dislike(self):
        self.assertTrue(self.bugurt.like(self.user, self.bugurt.id ,"dislike"))
        self.assertFalse(self.bugurt.like(self.user, self.bugurt.id ,"dislike"))

    def test_bugurttags(self):
        self.assertEqual(self.bugurttag.__unicode__(), "test")

    def test_bugurtproofs(self):
        self.assertEqual(self.bugurtproof.__unicode__(), "google.com")

    def test_like(self):
        self.assertTrue(self.bugurt.like(self.user, self.bugurt.id ,"like"))
        self.assertEqual(Like.objects.get(bugurt_id=self.bugurt.id).__unicode__(), "root1 : test")

    def test_dislike(self):
        self.assertTrue(self.bugurt.like(self.user, self.bugurt.id ,"like"))
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
