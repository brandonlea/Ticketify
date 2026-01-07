from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class UserAuthenticationTest(TestCase):
    """Test suite for user authentication"""

    def setUp(self):
        """Set up test data and client"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_user_registration_view(self):
        """Test user can access registration page"""
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)

    def test_user_login_view(self):
        """Test user can access login page"""
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)

    def test_user_can_login(self):
        """Test user can login with correct credentials"""
        login_successful = self.client.login(
            username='testuser',
            password='testpass123'
        )
        self.assertTrue(login_successful)

    def test_user_cannot_login_with_wrong_password(self):
        """Test user cannot login with incorrect password"""
        login_successful = self.client.login(
            username='testuser',
            password='wrongpassword'
        )
        self.assertFalse(login_successful)

    def test_user_logout(self):
        """Test user can logout"""
        # First login
        self.client.login(username='testuser', password='testpass123')

        # Then logout
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout

    def test_authenticated_user_redirected_from_login(self):
        """Test authenticated users are redirected away from login page"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:login'))
        # Should redirect to home if already logged in
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_redirected_from_register(self):
        """Test authenticated users are redirected away from register page"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:register'))
        # Should redirect to home if already logged in
        self.assertEqual(response.status_code, 302)