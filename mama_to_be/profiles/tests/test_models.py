from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from mama_to_be.profiles.models import AppUser, Profile


class AppUserModelTests(TestCase):

    def setUp(self):
        # Create a test user instance
        self.user = AppUser.objects.create_user(
            email="testuser@example.com",
            password="testpassword"
        )

    def test_app_user_creation(self):
        """Test that the AppUser instance is created correctly."""
        self.assertEqual(self.user.email, "testuser@example.com")
        self.assertTrue(self.user.check_password("testpassword"))
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertIsNotNone(self.user.date_joined)

    def test_str_method(self):
        """Test the __str__ method of the AppUser model."""
        self.assertEqual(str(self.user), "testuser@example.com")

    def test_default_is_active(self):
        """Test that the default value of is_active is True."""
        user = AppUser.objects.create_user(email="activeuser@example.com", password="testpassword")
        self.assertTrue(user.is_active)

    def test_last_login_field(self):
        """Test that last_login field is properly set."""
        user = AppUser.objects.create_user(email="newuser@example.com", password="testpassword")
        self.assertIsNone(user.last_login)  # Should be None initially

        user.last_login = timezone.now()
        user.save()
        self.assertIsNotNone(user.last_login)


class ProfileModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a user; the profile should be automatically created through the signal
        cls.user = AppUser.objects.create_user(
            email="testuser@example.com",
            password="testpassword"
        )

    def test_profile_creation(self):
        """Test that a profile is automatically created when a user is created."""
        # Fetch the profile that is created automatically by the signal
        profile = Profile.objects.get(user=self.user)

        # Check that the profile's user is the one we created
        self.assertEqual(profile.user.email, "testuser@example.com")

        # Check the default values for the profile fields
        self.assertIsNone(profile.username)
        self.assertIsNone(profile.description)
        self.assertEqual(profile.profile_picture.name, 'profile_pictures/381A0560.jpg')  # Default image path

    def test_str_method(self):
        profile = Profile.objects.get(user=self.user)
        """Test the __str__ method of the Profile model."""
        self.assertEqual(str(profile), f"Profile of {self.user.email}")

    def test_profile_with_username(self):
        profile = Profile.objects.get(user=self.user)
        """Test the Profile model with a username."""
        profile.username = "testuser123"
        profile.save()
        self.assertEqual(str(profile), "Profile of testuser123")


    def test_unique_username(self):
        """Test that the username field is unique across all profiles."""
        # Set a username for the first profile
        profile = Profile.objects.get(user=self.user)
        profile.username = "uniqueusername"
        profile.save()

        # Create a second user and their profile
        user2 = AppUser.objects.create_user(email="user2@example.com", password="password123")
        profile2 = Profile.objects.get(user=user2)

        # Attempt to set the same username for the second user profile
        profile2.username = "uniqueusername"

        # Ensure that saving the profile with a duplicate username raises an IntegrityError
        with self.assertRaises(IntegrityError):
            profile2.save()
