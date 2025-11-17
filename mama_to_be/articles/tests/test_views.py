from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from mama_to_be.articles.models import Article


class ArticleCreateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='testuser@test.com', password='testpassword')
        self.url = reverse('create-article')

    def test_create_article(self):
        # Ensure the user is logged in
        self.client.login(email='testuser@test.com', password='testpassword')

        # Data for the article creation form
        data = {
            'title': 'Test Article',
            'slug': 'test-article',
            'content': 'This is the content of the test article.',
            'category': 'Food',  # Ensure this matches your model choices
            'is_published': True,
        }

        # Make a POST request to create the article
        response = self.client.post(self.url, data)

        # Check if the article is created and redirected to the home page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

        # Verify the article is in the database
        article = Article.objects.first()
        self.assertEqual(article.title, 'Test Article')
        self.assertEqual(article.author, self.user)


class ArticleEditViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='testuser@test.com', password='testpassword')
        self.other_user = get_user_model().objects.create_user(email='otheruser@test.com', password='otherpassword')
        self.article = Article.objects.create(
            title='Test Article',
            slug='test-article',
            content='This is the content of the test article.',
            author=self.user,
            is_published=True
        )
        self.url = reverse('article-edit', kwargs={'slug': self.article.slug})

    def test_edit_article_by_author(self):
        # Ensure the user is logged in
        self.client.login(email='testuser@test.com', password='testpassword')

        # Edit article content
        data = {
            'title': 'Updated Article Title',
            'slug': 'updated-article-title',
            'content': 'This is the updated content of the test article.',
            'category': 'Health',
            'is_published': True,
        }

        response = self.client.post(self.url, data)

        # Ensure that the response redirects to the article detail page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('article-detail', kwargs={'slug': self.article.slug}))

        # Verify the article is updated
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, 'Updated Article Title')

    def test_edit_article_by_non_author(self):
        # Ensure a non-author cannot edit the article
        self.client.login(email='otheruser@test.com', password='otherpassword')

        response = self.client.get(self.url)

        # The response should be forbidden
        self.assertEqual(response.status_code, 403)


class ArticleDisplayViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='testuser@test.com', password='testpassword')
        self.article = Article.objects.create(
            title='Test Article',
            slug='test-article',
            content='This is the content of the test article.',
            author=self.user,
            is_published=True
        )
        self.url = reverse('article-detail', kwargs={'slug': self.article.slug})

    def test_article_detail_view(self):
        # Ensure the article is displayed correctly
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.article.title)
        self.assertContains(response, self.article.content)


class CategoryArticlesViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='testuser@test.com', password='testpassword')
        self.category = 'Health'
        self.article1 = Article.objects.create(
            title='Article 1',
            slug='article-1',
            content='Content of article 1',
            category=self.category,
            author=self.user,
            is_published=True,
            published_at=timezone.now() - timezone.timedelta(days=1)
        )
        self.article2 = Article.objects.create(
            title='Article 2',
            slug='article-2',
            content='Content of article 2',
            category=self.category,
            author=self.user,
            is_published=True,
            published_at=timezone.now()
        )
        self.url = reverse('category-articles', kwargs={'category': self.category})

    def test_category_articles_view(self):
        # Ensure the user is logged in
        self.client.login(email='testuser@test.com', password='testpassword')

        # Make the request
        response = self.client.get(self.url)

        # Check the status code
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.article1.title)
        self.assertContains(response, self.article2.title)
        self.assertEqual(len(response.context['page_obj']), 2)  # Ensure pagination works

    def test_invalid_category_raises_404(self):
        response = self.client.get(reverse('category-articles', kwargs={'category': 'invalid-category'}))
        self.assertEqual(response.status_code, 404)

    def test_pagination(self):
        category = 'Food'
        for i in range(20):  # Create more articles to test pagination
            Article.objects.create(title=f"Article {i}", category=category, is_published=True)

        response = self.client.get(reverse('category-articles', kwargs={'category': category}), {'page': 2})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Article 10")  # Check if the second page contains the correct article
