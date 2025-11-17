import uuid

from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import datetime
from django.utils import timezone

from mama_to_be.articles.models import Article


# Model tests


class ArticleModelTest(TestCase):
    def setUp(self):
        # Generate a unique email for the test user using uuid
        unique_email = f'testuser-{uuid.uuid4().hex}@test.com'
        self.user = get_user_model().objects.create_user(email=unique_email, password='testpassword')
        self.article_data = {
            'title': 'Test Article',
            'content': '<p>This is a test article.</p>',
            'author': self.user,
            'media_urls': '',
            'thumbnail_url': 'http://example.com/thumbnail.jpg',
            'category': 'TECH',
            'is_published': True,
        }

    def test_article_creation(self):
        # Create the article
        article = Article.objects.create(**self.article_data)

        # Check if the article is created correctly
        self.assertEqual(article.title, 'Test Article')
        self.assertEqual(article.content, '<p>This is a test article.</p>')
        self.assertEqual(article.author, self.user)
        self.assertEqual(article.category, 'TECH')
        self.assertTrue(article.is_published)

    def test_slug_generation(self):
        # Create an article without a slug
        article = Article.objects.create(**self.article_data)

        # Check if the slug is generated
        self.assertEqual(article.slug, 'test-article')

    def test_article_published_at(self):
        # Create an article and check if 'published_at' is None by default
        article = Article.objects.create(**self.article_data)
        self.assertIsNone(article.published_at)

        # Set the article as published
        article.published_at = timezone.now()
        article.save()

        # Check if 'published_at' is set
        self.assertIsNotNone(article.published_at)
        self.assertTrue(isinstance(article.published_at, datetime))

    def test_article_meta_ordering(self):
        # Create articles with specific 'published_at' times
        article1 = Article.objects.create(
            **self.article_data,
            created_at=timezone.now() - timezone.timedelta(days=1),
            published_at=timezone.now() - timezone.timedelta(days=2)  # Explicitly set published_at
        )
        article2 = Article.objects.create(
            **self.article_data,
            created_at=timezone.now(),
            published_at=timezone.now()  # Explicitly set published_at
        )

        # Check if the articles are ordered by 'published_at' in descending order
        articles = Article.objects.all()
        self.assertEqual(articles[0], article2)  # Most recently published article should come first
        self.assertEqual(articles[1], article1)

    def test_article_thumbnail_url(self):
        # Create an article with a thumbnail URL
        article = Article.objects.create(**self.article_data)

        # Check if the thumbnail URL is correct
        self.assertEqual(article.thumbnail_url, 'http://example.com/thumbnail.jpg')

    def test_article_author_nullable(self):
        # Create an article with no author (author is set to null)
        article_data_without_author = self.article_data.copy()
        article_data_without_author['author'] = None
        article = Article.objects.create(**article_data_without_author)

        # Check if the author field is nullable
        self.assertIsNone(article.author)

    def test_article_save_method(self):
        # Create an article without a slug
        article = Article.objects.create(**self.article_data)

        # Check if the slug is correctly set
        self.assertEqual(article.slug, 'test-article')

