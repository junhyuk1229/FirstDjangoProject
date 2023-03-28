from django.db.utils import IntegrityError
from django.test import TestCase, Client
from users.models import User, Profile
from django.urls import reverse

#region models

class CheckUsersModelUser(TestCase):
    @classmethod
    def setUp(self):
        temp_user = User.objects.create(username='TestUser')
        temp_user.set_password('tuse')
        temp_user.save()

    def test_user_created_check(self):
        User.objects.get(pk=1)

    def test_user_only_one_created_check(self):
        with self.assertRaises(IndexError):
            User.objects.all()[1]

    def test_auto_profile_creation_check(self):
        Profile.objects.get(user=User.objects.get(pk=1))

    def test_user_login_correct_info(self):
        temp_client = Client()
        self.assertEqual(True, temp_client.login(username='TestUser', password='tuse'))

    def test_user_login_case_sensitive_check(self):
        temp_client = Client()
        self.assertEqual(False, temp_client.login(username='Testuser', password='tuse'))
        self.assertEqual(False, temp_client.login(username='TestUser', password='use'))


class CheckUsersModelProfile(TestCase):
    @classmethod
    def setUp(self):
        User.objects.create(username='TestUser')

    def test_profile_only_one_created_check(self):
        Profile.objects.get(user=User.objects.get(pk=1))

    def test_profile_created_check(self):
        with self.assertRaises(IndexError):
            Profile.objects.all()[1]

    def test_profile_same_user_error_check(self):
        temp_user = User.objects.get(pk=1)
        with self.assertRaises(IntegrityError):
            Profile.objects.create(user=temp_user)

    def test_profile_default_img_link_check(self):
        temp_profile = Profile.objects.get(user=User.objects.get(pk=1))
        self.assertEqual(temp_profile.image.url, '/media/default.jpg')

#endregion

#region views

class CheckUsersViewLoginPage(TestCase):
    @classmethod
    def setUp(self):
        temp_user = User.objects.create(username='TestUser')
        temp_user.set_password('tuse')
        temp_user.save()
    
    def test_users_login_page_status_check_before_login(self):
        temp_client = Client()
        temp_resp = temp_client.get("/login/")
        self.assertEqual(temp_resp.status_code, 200)

    def test_users_login_page_status_check_after_login(self):
        temp_client = Client()
        temp_resp = temp_client.post("/login/", data={"username": "TestUser", "password": "tuse"})
        self.assertEqual(temp_resp.status_code, 302)

    def test_users_login_page_status_check_reverse(self):
        temp_client = Client()
        temp_resp = temp_client.get(reverse('user_login'))
        self.assertEqual(temp_resp.status_code, 200)

    def test_users_login_page_redirect_check(self):
        temp_client = Client()
        temp_resp = temp_client.post("/login/", data={"username": "TestUser", "password": "tuse"})
        self.assertEqual(temp_resp.url, "/school/")

    def test_users_login_page_wrong_login_check(self):
        temp_client = Client()
        temp_resp = temp_client.post("/login/", data={"username": "TestUser", "password": "use"})
        self.assertContains(temp_resp, "Please enter a correct username and password. Note that both fields may be case-sensitive.", html=True)


class CheckUsersViewLogoutPage(TestCase):
    def test_users_logout_page_status_check(self):
        temp_client = Client()
        temp_resp = temp_client.get("/logout/")
        self.assertEqual(temp_resp.status_code, 200)

    def test_reverse_logout_page_status_check_reverse(self):
        temp_client = Client()
        temp_resp = temp_client.get(reverse('user_logout'))
        self.assertEqual(temp_resp.status_code, 200)


class CheckUsersViewRegisterPage(TestCase):
    def test_users_register_page_status_check(self):
        temp_client = Client()
        temp_resp = temp_client.get("/register/")
        self.assertEqual(temp_resp.status_code, 200)

    def test_users_register_page_status_check_reverse(self):
        temp_client = Client()
        temp_resp = temp_client.get(reverse('user_register'))
        self.assertEqual(temp_resp.status_code, 200)

    def test_users_register_page_redirect(self):
        temp_client = Client()
        temp_resp = temp_client.post("/register/", data={
            "username": "TestUser",
            "password1": "testpass123",
            "password2": "testpass123",
            "email": "test@gmail.com",
            "first_name": "Kim",
            "last_name": "Jun",
        })
        self.assertEqual(temp_resp.url, '/login/')

    def test_users_register_page_register_check(self):
        temp_client = Client()
        temp_resp = temp_client.post("/register/", data={
            "username": "TestUser",
            "password1": "testpass123",
            "password2": "testpass123",
            "email": "test@gmail.com",
            "first_name": "Kim",
            "last_name": "Jun",
        })
        User.objects.get(pk=1)

    def test_users_register_page_register_correct_info(self):
        temp_client = Client()
        temp_resp = temp_client.post("/register/", data={
            "username": "TestUser",
            "password1": "testpass123",
            "password2": "testpass123",
            "email": "test@gmail.com",
            "first_name": "Kim",
            "last_name": "Jun",
        })
        self.assertEqual(temp_resp.status_code, 302)

    def test_users_register_page_register_wrong_email(self):
        temp_client = Client()
        temp_resp = temp_client.post("/register/", data={
            "username": "TestUser",
            "password1": "testpass123",
            "password2": "testpass123",
            "email": "test@gmail",
            "first_name": "Kim",
            "last_name": "Jun",
        })
        self.assertEqual(temp_resp.status_code, 200)
        self.assertContains(temp_resp, "Enter a valid email address.", html=True)

    def test_users_register_page_register_different_password(self):
        temp_client = Client()
        temp_resp = temp_client.post("/register/", data={
            "username": "TestUser",
            "password1": "testpass123",
            "password2": "testpass13",
            "email": "test@gmail.com",
            "first_name": "Kim",
            "last_name": "Jun",
        })
        self.assertEqual(temp_resp.status_code, 200)
        self.assertContains(temp_resp, "The two password fields didn’t match.", html=True)

    def test_users_register_page_register_same_username(self):
        User.objects.create(username='TestUser')
        temp_client = Client()
        temp_resp = temp_client.post("/register/", data={
            "username": "TestUser",
            "password1": "testpass123",
            "password2": "testpass123",
            "email": "test@gmail.com",
            "first_name": "Kim",
            "last_name": "Jun",
        })
        self.assertEqual(temp_resp.status_code, 200)
        self.assertContains(temp_resp, "A user with that username already exists.", html=True)

    def test_users_register_page_register_username_valid_symbol(self):
        temp_client = Client()
        temp_resp = temp_client.post("/register/", data={
            "username": "Test(*&%^(*&^%*))",
            "password1": "testpass123",
            "password2": "testpass123",
            "email": "test@gmail.com",
            "first_name": "Kim",
            "last_name": "Jun",
        })
        self.assertEqual(temp_resp.status_code, 200)
        self.assertContains(temp_resp, "Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.", html=True)


class CheckUsersViewProfilePage(TestCase):
    @classmethod
    def setUp(self):
        temp_client = Client()
        temp_client.post("/register/", data={
            "username": "TestUser",
            "password1": "testpass123",
            "password2": "testpass123",
            "email": "test@gmail.com",
            "first_name": "Kim",
            "last_name": "Jun",
        })
    
    def test_users_profile_page_status_check_before_login(self):
        temp_client = Client()
        temp_resp = temp_client.get("/profile/")
        self.assertEqual(temp_resp.status_code, 302)
        
    def test_users_profile_page_status_check_after_login(self):
        temp_client = Client()
        temp_client.login(username='TestUser', password='testpass123')
        temp_resp = temp_client.get("/profile/")
        self.assertEqual(temp_resp.status_code, 200)

    def test_users_profile_page_status_check_reverse(self):
        temp_client = Client()
        temp_resp = temp_client.get(reverse('user_profile'))
        self.assertEqual(temp_resp.status_code, 302)

    def test_users_profile_page_redirect_before_login(self):
        temp_client = Client()
        temp_resp = temp_client.get("/profile/")
        self.assertEqual(temp_resp.url, "/login/?next=/profile/")

    def test_users_profile_change_user_data(self):
        temp_client = Client()
        temp_client.login(username='TestUser', password='testpass123')
        temp_recv = temp_client.post('/profile/', data={
            "username": "TestChangedUser",
            "email": "test123@gmail.com",
        })
        self.assertEqual(temp_recv.status_code, 302)
        self.assertEqual(temp_recv.url, '/profile/')
        self.assertEqual(User.objects.get(pk=1).username, "TestChangedUser")
        self.assertEqual(User.objects.get(pk=1).email, "test123@gmail.com")

#endregion

