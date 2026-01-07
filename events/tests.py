from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.urls import reverse
from datetime import timedelta
from .models import Category, Event


class CategoryModelTest(TestCase):
    """Test suite for Category model"""

    def setUp(self):
        """Set up test data"""
        self.category = Category.objects.create(
            name='Music',
            description='Music events and concerts'
        )

    def test_category_creation(self):
        """Test category is created correctly"""
        self.assertEqual(self.category.name, 'Music')
        self.assertEqual(self.category.description, 'Music events and concerts')
        self.assertIsNotNone(self.category.created_at)

    def test_category_slug_auto_generation(self):
        """Test slug is automatically generated from name"""
        self.assertEqual(self.category.slug, 'music')

    def test_category_str_method(self):
        """Test string representation of category"""
        self.assertEqual(str(self.category), 'Music')

    def test_category_unique_name(self):
        """Test category name must be unique"""
        with self.assertRaises(Exception):
            Category.objects.create(
                name='Music',
                description='Another music category'
            )

    def test_category_ordering(self):
        """Test categories are ordered by name"""
        Category.objects.create(name='Sports')
        Category.objects.create(name='Arts')
        categories = Category.objects.all()
        self.assertEqual(categories[0].name, 'Arts')
        self.assertEqual(categories[1].name, 'Music')
        self.assertEqual(categories[2].name, 'Sports')


class EventModelTest(TestCase):
    """Test suite for Event model"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Music')
        self.future_date = timezone.now() + timedelta(days=30)

        self.event = Event.objects.create(
            category=self.category,
            title='Test Concert',
            description='A great test concert',
            venue='Test Arena',
            address='123 Test Street',
            city='Dublin',
            country='Ireland',
            event_date=self.future_date,
            capacity=1000,
            created_by=self.user
        )

    def test_event_creation(self):
        """Test event is created correctly"""
        self.assertEqual(self.event.title, 'Test Concert')
        self.assertEqual(self.event.venue, 'Test Arena')
        self.assertEqual(self.event.city, 'Dublin')
        self.assertEqual(self.event.capacity, 1000)
        self.assertTrue(self.event.is_active)

    def test_event_slug_auto_generation(self):
        """Test slug is automatically generated from title"""
        self.assertEqual(self.event.slug, 'test-concert')

    def test_event_slug_uniqueness(self):
        """Test unique slugs are generated for duplicate titles"""
        event2 = Event.objects.create(
            category=self.category,
            title='Test Concert',
            description='Another concert',
            venue='Test Arena 2',
            address='456 Test Street',
            city='Cork',
            event_date=self.future_date,
            capacity=500,
            created_by=self.user
        )
        self.assertEqual(event2.slug, 'test-concert-1')

    def test_event_str_method(self):
        """Test string representation of event"""
        expected = f"Test Concert - {self.future_date.strftime('%d %b %Y')}"
        self.assertEqual(str(self.event), expected)

    def test_event_absolute_url(self):
        """Test get_absolute_url method"""
        url = self.event.get_absolute_url()
        expected_url = reverse('events:event_detail', kwargs={'slug': self.event.slug})
        self.assertEqual(url, expected_url)

    def test_event_is_past_property(self):
        """Test is_past property returns correct value"""
        # Future event should not be past
        self.assertFalse(self.event.is_past)

    def test_event_category_relationship(self):
        """Test event category foreign key relationship"""
        self.assertEqual(self.event.category, self.category)
        self.assertIn(self.event, self.category.events.all())

    def test_event_created_by_relationship(self):
        """Test event creator foreign key relationship"""
        self.assertEqual(self.event.created_by, self.user)
        self.assertIn(self.event, self.user.created_events.all())

    def test_event_capacity_positive(self):
        """Test event capacity can be updated"""
        self.event.capacity = 1500
        self.event.save()
        self.assertEqual(self.event.capacity, 1500)

    def test_event_ordering(self):
        """Test events are ordered by event_date"""
        event2 = Event.objects.create(
            title='Earlier Event',
            description='An earlier event',
            venue='Test Venue',
            address='Test Address',
            city='Dublin',
            event_date=timezone.now() + timedelta(days=10),
            capacity=500
        )
        events = Event.objects.all()
        self.assertEqual(events[0], event2)
        self.assertEqual(events[1], self.event)


class EventViewsTest(TestCase):
    """Test suite for Event views"""

    def setUp(self):
        """Set up test data and client"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Music')
        self.event = Event.objects.create(
            category=self.category,
            title='Test Concert',
            description='A great test concert',
            venue='Test Arena',
            address='123 Test Street',
            city='Dublin',
            event_date=timezone.now() + timedelta(days=30),
            capacity=1000
        )

    def test_event_list_view(self):
        """Test event list view returns correct response"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Concert')

    def test_event_detail_view(self):
        """Test event detail view returns correct response"""
        response = self.client.get(
            reverse('events:event_detail', kwargs={'slug': self.event.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Concert')
        self.assertContains(response, 'Test Arena')
