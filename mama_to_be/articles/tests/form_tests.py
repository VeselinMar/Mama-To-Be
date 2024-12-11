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

    def test_clean_thumbnail_url_invalid_domain(self):
        form_data = {
            'title': 'Test Article',
            'content': 'This is the content of the test article.',
            'category': 'Food',
            'is_published': True,
            'thumbnail_url': 'https://untrustedsite.com/photo/abc123'
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

    def test_clean_media_urls_invalid_domain(self):
        form_data = {
            'title': 'Test Article',
            'content': 'This is the content of the test article.',
            'category': 'Food',
            'is_published': True,
            'media_urls': 'http://example.com/video1, https://shopify.com/video2'
        }
        form = ArticleForm(data=form_data)
        self.assertFalse(form.is_valid())  # The form should be invalid
        self.assertIn('media_urls', form.errors)  # 'media_urls' should be in the form errors
        self.assertIn("URL 'http://example.com/video1' is not from a trusted source.", form.errors['media_urls'])

    def test_clean_media_urls_exceeds_max_count(self):
        urls = ', '.join(['https://youtube.com/video'] * 11)  # 11 URLs, exceeds the limit
        form_data = {
            'title': 'Test Article',
            'content': 'This is the content of the test article.',
            'category': 'Food',
            'is_published': True,
            'media_urls': urls
        }
        form = ArticleForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('media_urls', form.errors)

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
