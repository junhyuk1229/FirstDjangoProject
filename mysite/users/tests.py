from django.test import TestCase, Client
from users.models import User, Profile
from django.urls import reverse


class CheckCreateModelUser(TestCase):
    @classmethod
    def setUp(self):
        temp_user = User.objects.create(username='Jun')
        temp_user.set_password('test123')
        temp_user.save()

    def test_user_created_check(self):
        User.objects.get(pk=1)

    def test_user_only_one_created_check(self):
        with self.assertRaises(IndexError):
            User.objects.all()[1]

    def test_user_instance_check(self):
        temp_user = User.objects.get(pk=1)
        self.assertTrue(isinstance(temp_user, User))

    def test_user_unicode_return_check(self):
        temp_user = User.objects.get(pk=1)
        self.assertEqual(temp_user.__unicode__(), temp_user.username)

    def test_user_string_return_check(self):
        temp_user = User.objects.get(pk=1)
        self.assertEqual(temp_user.__str__(), temp_user.username)

    def test_auto_profile_creation_check(self):
        Profile.objects.get(user=User.objects.get(pk=1))


class CheckCreateModelProfile(TestCase):
    @classmethod
    def setUp(self):
        User.objects.create(username='Jun')

    def test_profile_only_one_created_check(self):
        Profile.objects.get(user=User.objects.get(pk=1))

    def test_profile_not_created_check(self):
        with self.assertRaises(IndexError):
            Profile.objects.all()[1]

    def test_profile_instance_check(self):
        temp_profile = Profile.objects.get(user=User.objects.get(pk=1))
        self.assertTrue(isinstance(temp_profile, Profile))

    def test_profile_unicode_return_check(self):
        temp_profile = Profile.objects.get(user=User.objects.get(pk=1))
        self.assertEqual(temp_profile.__unicode__(), f'{temp_profile.user.username} Profile')

    def test_profile_string_return_check(self):
        temp_profile = Profile.objects.get(user=User.objects.get(pk=1))
        self.assertEqual(temp_profile.__str__(), f'{temp_profile.user.username} Profile')

    def test_profile_default_img_link_check(self):
        temp_profile = Profile.objects.get(user=User.objects.get(pk=1))
        self.assertEqual(temp_profile.image.url, '/media/default.jpg')


class CheckLoginUser(TestCase):
    @classmethod
    def setUp(self):
        temp_user = User.objects.create(username='Jun')
        temp_user.set_password('Kim')
        temp_user.save()
    
    def test_user_login_correct_info(self):
        temp_client = Client()
        self.assertEqual(True, temp_client.login(username='Jun', password='Kim'))

    def test_user_login_case_sensitive_check(self):
        temp_client = Client()
        self.assertEqual(False, temp_client.login(username='jun', password='Kim'))
        self.assertEqual(False, temp_client.login(username='Jun', password='kim'))
        self.assertEqual(False, temp_client.login(username='Jun', password='KiM'))
        self.assertEqual(False, temp_client.login(username='JUn', password='kim'))


class CheckBeforeLoginWebStatusCode(TestCase):
    def test_users_login_page_status_check_before_login(self):
        temp_client = Client()
        temp_resp = temp_client.post("/login/")
        self.assertEqual(temp_resp.status_code, 200)
    
    def test_users_logout_page_status_check_before_login(self):
        temp_client = Client()
        temp_resp = temp_client.post("/logout/")
        self.assertEqual(temp_resp.status_code, 200)
    
    def test_users_profile_page_status_check_before_login(self):
        temp_client = Client()
        temp_resp = temp_client.post("/profile/")
        self.assertEqual(temp_resp.status_code, 302)
        self.assertEqual(temp_resp.url, "/login/?next=/profile/")
    
    def test_users_register_page_status_check_before_login(self):
        temp_client = Client()
        temp_resp = temp_client.post("/register/")
        self.assertEqual(temp_resp.status_code, 200)


class CheckAfterLoginWebStatusCode(TestCase):
    @classmethod
    def setUp(self):
        temp_user = User.objects.create(username='Jun')
        temp_user.set_password('Kim')
        temp_user.save()
    
    def test_users_profile_page_status_check_after_login(self):
        temp_client = Client()
        temp_client.login(username='Jun', password='Kim')
        temp_resp = temp_client.get("/profile/")
        self.assertEqual(temp_resp.status_code, 200)


class CheckReverseWebStatusCode(TestCase):
    def test_reverse_login_page_status_check(self):
        temp_client = Client()
        temp_resp = temp_client.get(reverse('user_login'))
        self.assertEqual(temp_resp.status_code, 200)
    
    def test_reverse_logout_page_status_check(self):
        temp_client = Client()
        temp_resp = temp_client.get(reverse('user_logout'))
        self.assertEqual(temp_resp.status_code, 200)
    
    def test_reverse_profile_page_status_check(self):
        temp_client = Client()
        temp_resp = temp_client.get(reverse('user_profile'))
        self.assertEqual(temp_resp.status_code, 302)
    
    def test_reverse_register_page_status_check(self):
        temp_client = Client()
        temp_resp = temp_client.get(reverse('user_register'))
        self.assertEqual(temp_resp.status_code, 200)


class CheckViewLoginPage(TestCase):
    @classmethod
    def setUp(self):
        temp_user = User.objects.create(username='Jun')
        temp_user.set_password('Kim')
        temp_user.save()
    
    def test_users_login_page_login_check(self):
        temp_client = Client()
        temp_client.post("/login/", data={"username": "Jun", "password": "Kim"})

    def test_users_login_page_wrong_login_check(self):
        temp_client = Client()
        temp_resp = temp_client.post("/login/", data={"username": "jun", "password": "Kim"})
        self.assertEqual(temp_resp.status_code, 200)
        self.assertContains(temp_resp, "Please enter a correct username and password. Note that both fields may be case-sensitive.", html=True)

    def test_users_login_page_status_code_check(self):
        temp_client = Client()
        temp_resp = temp_client.post("/login/", data={"username": "Jun", "password": "Kim"})
        self.assertEqual(temp_resp.status_code, 302)

    def test_users_login_page_redirect_check(self):
        temp_client = Client()
        temp_resp = temp_client.post("/login/", data={"username": "Jun", "password": "Kim"})
        self.assertEqual(temp_resp.url, "/school/")


class CheckViewRegisterPage(TestCase):
    def test_users_register_page_register_correct_info(self):
        temp_client = Client()
        temp_resp = temp_client.post("/register/", data={
            "username": "junkim",
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
            "username": "junkim",
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
            "username": "junkim",
            "password1": "testpass123",
            "password2": "testpass13",
            "email": "test@gmail.com",
            "first_name": "Kim",
            "last_name": "Jun",
        })
        self.assertEqual(temp_resp.status_code, 200)
        self.assertContains(temp_resp, "The two password fields didn’t match.", html=True)

    def test_users_register_page_register_same_username(self):
        User.objects.create(username='junkim')
        temp_client = Client()
        temp_resp = temp_client.post("/register/", data={
            "username": "junkim",
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
            "username": "jun(*&%^(*&^%*))",
            "password1": "testpass123",
            "password2": "testpass123",
            "email": "test@gmail.com",
            "first_name": "Kim",
            "last_name": "Jun",
        })
        self.assertEqual(temp_resp.status_code, 200)
        self.assertContains(temp_resp, "Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.", html=True)

    def test_users_register_page_register_check(self):
        temp_client = Client()
        temp_resp = temp_client.post("/register/", data={
            "username": "junkim",
            "password1": "testpass123",
            "password2": "testpass123",
            "email": "test@gmail.com",
            "first_name": "Kim",
            "last_name": "Jun",
        })
        self.assertEqual(temp_resp.status_code, 302)
        self.assertEqual(temp_resp.url, '/login/')
        User.objects.get(pk=1)

    def test_users_register_page_register_check_profile(self):
        temp_client = Client()
        temp_resp = temp_client.post("/register/", data={
            "username": "junkim",
            "password1": "testpass123",
            "password2": "testpass123",
            "email": "test@gmail.com",
            "first_name": "Kim",
            "last_name": "Jun",
        })
        Profile.objects.get(pk=1)


class CheckViewProfilePage(TestCase):
    @classmethod
    def setUp(self):
        temp_client = Client()
        temp_client.post("/register/", data={
            "username": "junkim",
            "password1": "testpass123",
            "password2": "testpass123",
            "email": "test@gmail.com",
            "first_name": "Kim",
            "last_name": "Jun",
        })
    
    def test_users_profile_check_correct_login(self):
        temp_client = Client()
        temp_client.login(username='junkim', password='testpass123')
        temp_recv = temp_client.get('/profile/')
        self.assertEqual(temp_recv.status_code, 200)

    def test_users_profile_check_wrong_login(self):
        temp_client = Client()
        temp_client.login(username='junkim', password='testpass23')
        temp_recv = temp_client.get('/profile/')
        self.assertEqual(temp_recv.status_code, 302)
        self.assertEqual(temp_recv.url, '/login/?next=/profile/')

    def test_users_profile_change_user_data(self):
        temp_client = Client()
        temp_client.login(username='junkim', password='testpass123')
        temp_recv = temp_client.post('/profile/', data={
            "username": "Junkim",
            "email": "test123@gmail.com",
        })
        self.assertEqual(temp_recv.status_code, 302)
        self.assertEqual(temp_recv.url, '/profile/')
        self.assertEqual(User.objects.get(pk=1).username, "Junkim")
        self.assertEqual(User.objects.get(pk=1).email, "test123@gmail.com")
