from django.contrib.auth import get_user_model
from django.test import TestCase


class UserTest(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email="user@gmail.com", password="pass")
        self.assertEqual(user.email, "user@gmail.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            user = User.objects.create_user()
        with self.assertRaises(TypeError):
            user = User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            user = User.objects.create_user(email="", password="pass")