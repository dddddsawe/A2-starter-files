# accounts/tests.py

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AuthViewTests(TestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.user_data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
        }
        self.user = get_user_model().objects.create_user(**self.user_data)

    def test_register_view(self):
        # Test GET request
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register')
        self.assertTemplateUsed(response, 'registration/register.html')

        # Test POST request with valid data
        response = self.client.post(self.register_url, data=self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

        # Test POST request with invalid data
        self.user_data['username'] = 'testuser'
        response = self.client.post(self.register_url, data=self.user_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A user with that username already exists')

    def test_login_view(self):
        # Test GET request
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Log in')
        self.assertTemplateUsed(response, 'registration/login.html')

        # Test POST request with valid data
        response = self.client.post(self.login_url, data={
            'username': 'testuser',
            'password': 'testpassword',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile'))

        # Test POST request with invalid data
        response = self.client.post(self.login_url, data={
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Username or password is invalid')

    def test_logout_view(self):
        # Test GET request when authenticated
        self.client.force_login(self.user)
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

        # Test GET request when unauthenticated
        self.client.logout()
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)


class ProfileViewTests(TestCase):
    def setUp(self):
        self.view_url = reverse('profile')
        self.edit_url = reverse('profile_edit')
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
        }
        self.user = get_user_model().objects.create_user(**self.user_data)

    def test_view_profile(self):
        # Test GET request when authenticated
        self.client.force_login(self.user)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test User')
        self.assertContains(response, 'testuser@example.com')
