from django.test import TestCase
from users.models import User, Profile
from django.urls import reverse
from datetime import datetime
from django.contrib.auth import views as auth_views


class CheckUserCreateGeneral(TestCase):
    def create_user(self, username='hapuhvphasktn'):
        return User.objects.create(username=username)

    def test_creation(self):
        temp_user = self.create_user()
        self.assertTrue(isinstance(temp_user, User))
        self.assertEqual(temp_user.__unicode__(), temp_user.username)
        self.assertEqual(temp_user.__str__(), temp_user.username)


class CheckUserCreateTime(TestCase):
    def create_user(self, username='hapuhvphaktn'):
        return User.objects.create(username=username)

    def test_creation(self):
        temp_user = self.create_user()
        self.assertEqual(temp_user.date_joined.year, datetime.now().year)
        self.assertEqual(temp_user.date_joined.month, datetime.now().month)
        self.assertEqual(temp_user.date_joined.day, datetime.now().day)
        self.assertEqual(temp_user.date_joined.hour, datetime.now().hour)
        self.assertEqual(temp_user.date_joined.month, datetime.now().month)


class CheckViewRegister(TestCase):
    def test_register(self):
        temp_view = auth_views.LoginView.as_view(template_name='users/user_login.html')
        temp_url = reverse("user_register")
        resp = self.client.get(temp_url)

        self.assertEqual(resp.status_code, 200)
        self.assertIn(temp_view, resp.content)


class CheckProfileCreateGeneral(TestCase):
    def create_user(self, username='vphasktn'):
        return User.objects.create(username=username)

    def test_creation(self):
        temp_user = self.create_user()
        temp_profile = Profile.objects.get(user=temp_user)
        self.assertTrue(isinstance(temp_profile, Profile))
        self.assertEqual(temp_profile.__unicode__(), f'{temp_profile.user.username} Profile')
        self.assertEqual(temp_profile.__str__(), f'{temp_profile.user.username} Profile')
        self.assertEqual(temp_profile.image.url, '/media/default.jpg')
