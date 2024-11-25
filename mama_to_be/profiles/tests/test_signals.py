from django.contrib.auth import get_user_model
from django.test import TestCase
from mama_to_be.profiles.models import Profile

UserModel = get_user_model()


class ProfileSignalTest(TestCase):
    def test_profile_created_on_user_creation(self):
        user = UserModel.objects.create_user(username="JohnDoe@gmail.com", password="Password14@7")
        self.assertTrue(Profile.objects.filter(user=user).exists())
