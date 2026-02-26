from django.test import TestCase

from mama_to_be.articles.forms import ArticleForm


class ArticleFormTests(TestCase):

    def test_clean_thumbnail_url_valid(self):
        form_data = {
            'title': 'Test Article',
            'content': 'This is the content of the test article.',
            'category': 'Food',
            'is_published': True,
            'thumbnail_url': 'https://unsplash.com/photo/abc123'
        }
        form = ArticleForm(data=form_data)
        self.assertTrue(form.is_valid())
        