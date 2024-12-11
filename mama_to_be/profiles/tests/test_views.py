from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from mama_to_be.articles.models import Article
from mama_to_be.profiles.models import Profile

User = get_user_model()


class RegisterViewTests(TestCase):

    def test_register_view_valid(self):
        """Test successful registration."""
        data = {
            'email': 'newuser@example.com',
            'password1': 'Password14@7',
            'password2': 'Password14@7',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 302)  # Redirects to profile edit
        self.assertRedirects(response, reverse('profile-edit'))
        user = User.objects.get(email='newuser@example.com')
        self.assertTrue(user.is_authenticated)


class UserRegistrationTests(TestCase):

    def test_register_view_invalid(self):
        """Test invalid registration (passwords do not match)."""
        data = {
            'email': 'newuser@example.com',
            'password1': 'Password14@7',
            'password2': 'WrongPassword',
        }
        response = self.client.post(reverse('register'), data)

        self.assertEqual(response.status_code, 200)  # Stays on the register page

        # Extract the form from the response context
        form = response.context.get('form')

        # Check if the form contains the correct error for the 'password2' field
        self.assertTrue(form.errors.get('password2'), "The two password fields didn’t match.")


class CustomLoginViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')

    def test_login_view_valid(self):
        """Test successful login."""
        data = {
            'username': 'testuser@example.com',
            'password': 'testpassword',
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 302)  # Redirect to home
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(self.client.session['_auth_user_id'])

    def test_login_view_invalid(self):
        """Test invalid login credentials."""
        data = {
            'username': 'testuser@example.com',
            'password': 'WrongPassword',
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 200)  # Stay on login page
        self.assertContains(response,
                            "Please enter a correct Email Address and password."
                            " Note that both fields may be case-sensitive.")


class CustomLogoutViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')

    def test_logout_view(self):
        """Test logout functionality."""
        self.client.login(email='testuser@example.com', password='testpassword')
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        self.assertFalse('_auth_user_id' in self.client.session)


class ProfileEditViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.profile = Profile.objects.get(user=self.user)
        self.client.login(email='testuser@example.com', password='testpassword')

    def test_profile_edit_view_valid(self):
        """Test successful profile edit."""
        data = {
            'username': 'newusername',
            'description': 'Updated description.',
        }

        # Update the test profile data
        response = self.client.post(reverse('profile-edit'), data)

        # Check that the response redirects to the correct profile display URL
        self.assertEqual(response.status_code, 302)  # Redirects to profile display
        self.assertRedirects(response,
                             reverse('profile-display', kwargs={'user_id': self.profile.user.id}))  # Pass the user_id

        # Refresh the profile from the database and check if the changes are saved
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.username, 'newusername')
        self.assertEqual(self.profile.description, 'Updated description.')


class ProfileDisplayViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.profile = Profile.objects.get(user=self.user)
        self.client.login(email='testuser@example.com', password='testpassword')

    def test_profile_display_view(self):
        """Test profile display view for logged-in user."""
        response = self.client.get(reverse('profile-display', kwargs={'user_id': self.user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.profile.username)
        self.assertContains(response, self.profile.description)

    def test_profile_display_view_another_user(self):
        """Test profile display view for another user's profile."""
        other_user = get_user_model().objects.create_user(
            email='otheruser@example.com',
            password='otherpassword'
        )
        other_profile = Profile.objects.get(user=other_user)
        response = self.client.get(reverse('profile-display', kwargs={'user_id': other_user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, other_profile.username)
        self.assertContains(response, other_profile.description)

    def test_profile_display_view_no_articles(self):
        """Test profile view when user has no published articles."""
        response = self.client.get(reverse('profile-display', kwargs={'user_id': self.user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No published articles available.")

    def test_profile_display_view_with_unpublished_articles(self):
        """Test profile view with unpublished articles (only visible for the owner)."""
        unpublished_article = Article.objects.create(
            title="Unpublished Article",
            author=self.user,
            is_published=False
        )
        response = self.client.get(reverse('profile-display', kwargs={'user_id': self.user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, unpublished_article.title)
