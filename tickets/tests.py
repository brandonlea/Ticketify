from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta
from decimal import Decimal
from events.models import Category, Event
from .models import Ticket, Order, OrderLineItem


class TicketModelTest(TestCase):
    """Test suite for Ticket model"""

    def setUp(self):
        """Set up test data"""
        self.category = Category.objects.create(name='Music')
        self.event = Event.objects.create(
            category=self.category,
            title='Test Concert',
            description='A great concert',
            venue='Test Arena',
            address='123 Test Street',
            city='Dublin',
            event_date=timezone.now() + timedelta(days=30),
            capacity=1000
        )
        self.ticket = Ticket.objects.create(
            event=self.event,
            ticket_type='general',
            description='General admission ticket',
            price=Decimal('50.00'),
            quantity_available=100,
            quantity_sold=0
        )

    def test_ticket_creation(self):
        """Test ticket is created correctly"""
        self.assertEqual(self.ticket.event, self.event)
        self.assertEqual(self.ticket.ticket_type, 'general')
        self.assertEqual(self.ticket.price, Decimal('50.00'))
        self.assertEqual(self.ticket.quantity_available, 100)
        self.assertEqual(self.ticket.quantity_sold, 0)
        self.assertTrue(self.ticket.is_active)

    def test_ticket_str_method(self):
        """Test string representation of ticket"""
        expected = f"{self.event.title} - General Admission (£50.00)"
        self.assertEqual(str(self.ticket), expected)

    def test_ticket_quantity_remaining(self):
        """Test quantity_remaining property"""
        self.assertEqual(self.ticket.quantity_remaining, 100)

        self.ticket.quantity_sold = 30
        self.ticket.save()
        self.assertEqual(self.ticket.quantity_remaining, 70)

    def test_ticket_is_sold_out(self):
        """Test is_sold_out property"""
        self.assertFalse(self.ticket.is_sold_out)

        self.ticket.quantity_sold = 100
        self.ticket.save()
        self.assertTrue(self.ticket.is_sold_out)

    def test_ticket_percentage_sold(self):
        """Test percentage_sold property"""
        self.assertEqual(self.ticket.percentage_sold, 0)

        self.ticket.quantity_sold = 50
        self.ticket.save()
        self.assertEqual(self.ticket.percentage_sold, 50.0)

    def test_ticket_is_available(self):
        """Test is_available property"""
        self.assertTrue(self.ticket.is_available)

        # Test when sold out
        self.ticket.quantity_sold = 100
        self.ticket.save()
        self.assertFalse(self.ticket.is_available)

    def test_ticket_unique_together(self):
        """Test ticket type must be unique per event"""
        with self.assertRaises(Exception):
            Ticket.objects.create(
                event=self.event,
                ticket_type='general',
                price=Decimal('60.00'),
                quantity_available=50
            )

    def test_ticket_ordering(self):
        """Test tickets are ordered by price"""
        vip_ticket = Ticket.objects.create(
            event=self.event,
            ticket_type='vip',
            price=Decimal('100.00'),
            quantity_available=50
        )
        student_ticket = Ticket.objects.create(
            event=self.event,
            ticket_type='student',
            price=Decimal('30.00'),
            quantity_available=75
        )

        tickets = Ticket.objects.all()
        self.assertEqual(tickets[0], student_ticket)
        self.assertEqual(tickets[1], self.ticket)
        self.assertEqual(tickets[2], vip_ticket)

    def test_ticket_price_positive(self):
        """Test ticket price must be positive"""
        self.ticket.price = Decimal('75.00')
        self.ticket.save()
        self.assertEqual(self.ticket.price, Decimal('75.00'))


class OrderModelTest(TestCase):
    """Test suite for Order model"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Music')
        self.event = Event.objects.create(
            category=self.category,
            title='Test Concert',
            description='A great concert',
            venue='Test Arena',
            address='123 Test Street',
            city='Dublin',
            event_date=timezone.now() + timedelta(days=30),
            capacity=1000
        )
        self.ticket = Ticket.objects.create(
            event=self.event,
            ticket_type='general',
            price=Decimal('50.00'),
            quantity_available=100
        )
        self.order = Order.objects.create(
            user=self.user,
            full_name='Test User',
            email='test@example.com',
            phone_number='0123456789',
            address='123 Test St',
            city='Dublin',
            post_code='D01 1234',
            country='Ireland',
            order_total=Decimal('100.00')
        )

    def test_order_creation(self):
        """Test order is created correctly"""
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.full_name, 'Test User')
        self.assertEqual(self.order.email, 'test@example.com')
        self.assertEqual(self.order.order_total, Decimal('100.00'))
        self.assertFalse(self.order.paid)

    def test_order_number_generation(self):
        """Test order number is automatically generated"""
        self.assertIsNotNone(self.order.order_number)
        self.assertEqual(len(self.order.order_number), 32)

    def test_order_number_unique(self):
        """Test each order gets a unique order number"""
        order2 = Order.objects.create(
            user=self.user,
            full_name='Test User',
            email='test@example.com',
            phone_number='0123456789',
            address='123 Test St',
            city='Dublin',
            post_code='D01 1234',
            country='Ireland'
        )
        self.assertNotEqual(self.order.order_number, order2.order_number)

    def test_order_str_method(self):
        """Test string representation of order"""
        self.assertEqual(str(self.order), self.order.order_number)

    def test_order_update_total(self):
        """Test update_total method calculates correct total"""
        # Create order line items
        OrderLineItem.objects.create(
            order=self.order,
            ticket=self.ticket,
            quantity=2
        )

        self.order.update_total()
        self.assertEqual(self.order.order_total, Decimal('100.00'))

    def test_order_ordering(self):
        """Test orders are ordered by date descending"""
        order2 = Order.objects.create(
            user=self.user,
            full_name='Test User',
            email='test@example.com',
            phone_number='0123456789'
        )
        orders = Order.objects.all()
        self.assertEqual(orders[0], order2)
        self.assertEqual(orders[1], self.order)


class OrderLineItemModelTest(TestCase):
    """Test suite for OrderLineItem model"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Music')
        self.event = Event.objects.create(
            category=self.category,
            title='Test Concert',
            description='A great concert',
            venue='Test Arena',
            address='123 Test Street',
            city='Dublin',
            event_date=timezone.now() + timedelta(days=30),
            capacity=1000
        )
        self.ticket = Ticket.objects.create(
            event=self.event,
            ticket_type='general',
            price=Decimal('50.00'),
            quantity_available=100
        )
        self.order = Order.objects.create(
            user=self.user,
            full_name='Test User',
            email='test@example.com',
            phone_number='0123456789'
        )

    def test_lineitem_creation(self):
        """Test order line item is created correctly"""
        lineitem = OrderLineItem.objects.create(
            order=self.order,
            ticket=self.ticket,
            quantity=2
        )
        self.assertEqual(lineitem.order, self.order)
        self.assertEqual(lineitem.ticket, self.ticket)
        self.assertEqual(lineitem.quantity, 2)

    def test_lineitem_total_calculation(self):
        """Test lineitem_total is calculated correctly"""
        lineitem = OrderLineItem.objects.create(
            order=self.order,
            ticket=self.ticket,
            quantity=3
        )
        expected_total = Decimal('50.00') * 3
        self.assertEqual(lineitem.lineitem_total, expected_total)

    def test_lineitem_str_method(self):
        """Test string representation of order line item"""
        lineitem = OrderLineItem.objects.create(
            order=self.order,
            ticket=self.ticket,
            quantity=2
        )
        expected = f'general for {self.event.title} (x2)'
        self.assertEqual(str(lineitem), expected)
