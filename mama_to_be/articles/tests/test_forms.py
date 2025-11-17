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

    def test_clean_thumbnail_url_invalid_scheme(self):
        form_data = {
            'title': 'Test Article',
            'content': 'This is the content of the test article.',
            'category': 'Food',
            'is_published': True,
            'thumbnail_url': 'ftp://unsplash.com/photo/abc123'
        }
        form = ArticleForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('thumbnail_url', form.errors)


    def test_clean_thumbnail_url_exceeds_max_length(self):
        long_url = 'https://unsplash.com/' + 'a' * 501  # Make URL too long
        form_data = {
            'title': 'Test Article',
            'content': 'This is the content of the test article.',
            'category': 'Food',
            'is_published': True,
            'thumbnail_url': long_url
        }
        form = ArticleForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('thumbnail_url', form.errors)

    def test_clean_media_urls_valid(self):
        form_data = {
            'title': 'Test Article',
            'content': 'This is the content of the test article.',
            'category': 'Food',
            'is_published': True,
            'media_urls': 'https://youtube.com/video1, https://vimeo.com/video2'
        }
        form = ArticleForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_clean_media_urls_exceeds_max_length(self):
        long_url = 'https://youtube.com/' + 'a' * 501  # Make URL too long
        form_data = {
            'title': 'Test Article',
            'content': 'This is the content of the test article.',
            'category': 'Food',
            'is_published': True,
            'media_urls': f'{long_url}, https://vimeo.com/video2'
        }
        form = ArticleForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('media_urls', form.errors)
