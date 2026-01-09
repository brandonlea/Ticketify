from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileModelTest(TestCase):
    """Test suite for UserProfile model"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_profile_auto_creation(self):
        """Test user profile is automatically created when user is created"""
        self.assertTrue(hasattr(self.user, 'userprofile'))
        self.assertIsInstance(self.user.userprofile, UserProfile)

    def test_profile_str_method(self):
        """Test string representation of profile"""
        self.assertEqual(str(self.user.userprofile), 'testuser')

    def test_profile_default_country(self):
        """Test profile has default country of Ireland"""
        self.assertEqual(self.user.userprofile.country, 'Ireland')

    def test_profile_update(self):
        """Test profile can be updated with user information"""
        profile = self.user.userprofile
        profile.phone_number = '0123456789'
        profile.street_address1 = '123 Test Street'
        profile.town_or_city = 'Dublin'
        profile.postcode = 'D01 1234'
        profile.save()

        # Refresh from database
        profile.refresh_from_db()

        self.assertEqual(profile.phone_number, '0123456789')
        self.assertEqual(profile.street_address1, '123 Test Street')
        self.assertEqual(profile.town_or_city, 'Dublin')
        self.assertEqual(profile.postcode, 'D01 1234')

    def test_profile_one_to_one_relationship(self):
        """Test profile has one-to-one relationship with user"""
        self.assertEqual(self.user.userprofile.user, self.user)

    def test_profile_deletion_when_user_deleted(self):
        """Test profile is deleted when user is deleted"""
        user_id = self.user.id
        self.user.delete()

        # Check profile no longer exists
        self.assertFalse(
            UserProfile.objects.filter(user_id=user_id).exists()
        )
