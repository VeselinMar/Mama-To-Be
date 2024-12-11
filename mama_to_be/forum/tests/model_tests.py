from django.test import TestCase
from django.contrib.auth import get_user_model

from mama_to_be.forum.models import Category, Topic, Discussion, Comment, Like

User = get_user_model()


class CategoryModelTest(TestCase):

    def test_category_slug_is_generated(self):
        category = Category.objects.create(name="Test Category")
        self.assertEqual(category.slug, "test-category")

    def test_category_slug_uniqueness(self):
        category1 = Category.objects.create(name="Test Category")
        category2 = Category.objects.create(name="Test Category 1")

        # Ensure both slugs are generated and unique
        self.assertNotEqual(category1.slug, category2.slug)
        self.assertTrue(category2.slug.startswith("test-category"))


class TopicModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="unique_testuser@example.com", password="password")
        self.category = Category.objects.create(name="Test Category")

    def test_topic_slug_is_generated(self):
        topic = Topic.objects.create(title="Test Topic", category=self.category, created_by=self.user)
        self.assertEqual(topic.slug, "test-topic")

    def test_topic_slug_uniqueness(self):
        Topic.objects.create(title="Test Topic", category=self.category, created_by=self.user)
        topic2 = Topic.objects.create(title="Test Topic", category=self.category, created_by=self.user)
        self.assertNotEqual(topic2.slug, "test-topic")
        self.assertTrue(topic2.slug.startswith("test-topic"))


class DiscussionModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="unique_testuser@example.com", password="password")
        self.category = Category.objects.create(name="Test Category")
        self.topic = Topic.objects.create(title="Test Topic", category=self.category, created_by=self.user)

    def test_discussion_creation(self):
        discussion = Discussion.objects.create(topic=self.topic, created_by=self.user, content="Test Content")
        self.assertEqual(discussion.topic, self.topic)
        self.assertEqual(discussion.created_by, self.user)
        self.assertEqual(discussion.content, "Test Content")


class CommentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="unique_testuser@example.com", password="password")
        self.category = Category.objects.create(name="Test Category")
        self.topic = Topic.objects.create(title="Test Topic", category=self.category, created_by=self.user)
        self.discussion = Discussion.objects.create(topic=self.topic, created_by=self.user, content="Test Content")

    def test_comment_creation(self):
        comment = Comment.objects.create(discussion=self.discussion, content="Test Comment", created_by=self.user)
        self.assertEqual(comment.discussion, self.discussion)
        self.assertEqual(comment.content, "Test Comment")
        self.assertEqual(comment.created_by, self.user)

    def test_comment_replies(self):
        parent_comment = Comment.objects.create(discussion=self.discussion, content="Parent Comment", created_by=self.user)
        reply = Comment.objects.create(discussion=self.discussion, content="Reply Comment", created_by=self.user, parent=parent_comment)
        self.assertEqual(reply.parent, parent_comment)
        self.assertIn(reply, parent_comment.replies.all())


class LikeModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="shefa@shefski.mail", password="password")
        self.category = Category.objects.create(name="Test Category")
        self.topic = Topic.objects.create(title="Test Topic", category=self.category, created_by=self.user)
        self.discussion = Discussion.objects.create(topic=self.topic, created_by=self.user, content="Test Content")
        self.comment = Comment.objects.create(discussion=self.discussion, content="Test Comment", created_by=self.user)

    def test_like_creation(self):
        like = Like.objects.create(comment=self.comment, user=self.user)
        self.assertEqual(like.comment, self.comment)
        self.assertEqual(like.user, self.user)

    def test_like_uniqueness(self):
        Like.objects.create(comment=self.comment, user=self.user)
        with self.assertRaises(Exception):
            Like.objects.create(comment=self.comment, user=self.user)
