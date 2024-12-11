from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from mama_to_be.articles.choices import CategoryChoices
from mama_to_be.articles.models import Article


class HomeViewTests(TestCase):

    def setUp(self):
        # Create a user (if needed for authenticated views)
        self.user = get_user_model().objects.create_user(email='testuser@pier.bg', password='password')

        # Create some categories
        self.category1 = CategoryChoices.FITNESS
        self.category2 = CategoryChoices.HEALTH

        # Create articles for each category
        self.article1 = Article.objects.create(
            title="Article 1",
            category=self.category1,
            content="Content of article 1",
            is_published=True,
            published_at="2024-12-10"
        )
        self.article2 = Article.objects.create(
            title="Article 2",
            category=self.category1,
            content="Content of article 2",
            is_published=True,
            published_at="2024-12-11"
        )
        self.article3 = Article.objects.create(
            title="Article 3",
            category=self.category1,
            content="Content of article 3",
            is_published=True,
            published_at="2024-12-12"
        )
        self.article4 = Article.objects.create(
            title="Article 4",
            category=self.category2,
            content="Content of article 4",
            is_published=True,
            published_at="2024-12-10"
        )
        self.article5 = Article.objects.create(
            title="Article 5",
            category=self.category2,
            content="Content of article 5",
            is_published=True,
            published_at="2024-12-11"
        )
        self.article6 = Article.objects.create(
            title="Article 6",
            category=self.category2,
            content="Content of article 6",
            is_published=True,
            published_at="2024-12-12"
        )

    def test_home_view_status_code(self):
        """Test that the view loads successfully and returns a 200 status code."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_template(self):
        """Test that the correct template is used."""
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'common/home.html')

    def test_articles_grouped_by_category(self):
        """Test that articles are grouped by category and each category has a maximum of 3 articles."""
        response = self.client.get(reverse('home'))
        self.assertEqual(len(response.context['articles_by_category']), 2)  # 2 categories
        self.assertEqual(len(response.context['articles_by_category'][self.category1]),
                         3)  # Max 3 articles for category1
        self.assertEqual(len(response.context['articles_by_category'][self.category2]),
                         3)  # Max 3 articles for category2

    def test_no_articles(self):
        """Test that if no articles exist, no articles are returned."""
        Article.objects.all().delete()  # Delete all articles
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['articles_by_category']), 0)  # No articles in any category

    def test_article_count_per_category(self):
        """Test that no more than 3 articles are fetched per category."""
        # Create more than 3 articles for one category
        self.article7 = Article.objects.create(
            title="Article 7",
            category=self.category1,
            content="Content of article 7",
            is_published=True,
            published_at="2024-12-13"
        )

        response = self.client.get(reverse('home'))
        self.assertEqual(len(response.context['articles_by_category'][self.category1]),
                         3)  # Should only return 3 articles
