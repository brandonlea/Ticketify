import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Sum
from events.models import Event


class Ticket(models.Model):
    """
    Ticket model representing different ticket types for events
    (e.g., General Admission, VIP, Early Bird, Student)
    """
    TICKET_TYPES = [
        ('general', 'General Admission'),
        ('vip', 'VIP'),
        ('early_bird', 'Early Bird'),
        ('student', 'Student'),
    ]

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='tickets'
    )
    ticket_type = models.CharField(max_length=50, choices=TICKET_TYPES)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    quantity_available = models.PositiveIntegerField()
    quantity_sold = models.PositiveIntegerField(default=0)
    sale_start_date = models.DateTimeField(null=True, blank=True)
    sale_end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['price']
        unique_together = ['event', 'ticket_type']

    def clean(self):
        """Validate ticket data"""
        errors = {}

        # Validate sale dates
        if self.sale_start_date and self.sale_end_date:
            if self.sale_end_date <= self.sale_start_date:
                errors['sale_end_date'] = 'Sale end date must be after sale start date.'

        # Validate quantity sold doesn't exceed available
        if self.quantity_available is not None and self.quantity_sold > self.quantity_available:
            errors['quantity_sold'] = 'Quantity sold cannot exceed quantity available.'

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """Run full_clean before saving"""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.event.title} - {self.get_ticket_type_display()} (£{self.price})"

    @property
    def quantity_remaining(self):
        """Calculate remaining tickets"""
        if self.quantity_available is None:
            return 0
        return self.quantity_available - self.quantity_sold

    @property
    def is_available(self):
        """Check if tickets are available for purchase"""
        now = timezone.now()

        # Check if active and has remaining quantity
        if not self.is_active or self.quantity_remaining <= 0:
            return False

        # Check sale date windows
        if self.sale_start_date and now < self.sale_start_date:
            return False

        if self.sale_end_date and now > self.sale_end_date:
            return False

        # Check if event is in the past
        if self.event.is_past:
            return False

        return True

    @property
    def is_sold_out(self):
        """Check if this ticket type is sold out"""
        return self.quantity_remaining == 0

    @property
    def percentage_sold(self):
        """Calculate percentage of tickets sold"""
        if self.quantity_available is None or self.quantity_available == 0:
            return 0
        return (self.quantity_sold / self.quantity_available) * 100


class Order(models.Model):
    """
    Order model representing a customer's ticket purchase
    """
    order_number = models.CharField(max_length=32, unique=True, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=50, default='')
    post_code = models.CharField(max_length=20, default='')
    country = models.CharField(max_length=50, default='')
    date = models.DateTimeField(auto_now_add=True)
    order_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    stripe_pid = models.CharField(max_length=254, default='')
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']

    def _generate_order_number(self):
        """Generate a random, unique order number using UUID"""
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        """Override save to set order number if not set"""
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def update_total(self):
        """Update order total based on line items"""
        self.order_total = self.lineitems.aggregate(
            Sum('lineitem_total')
        )['lineitem_total__sum'] or 0
        self.save()

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    """
    OrderLineItem model representing individual tickets in an order
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='lineitems'
    )
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    lineitem_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False
    )

    def save(self, *args, **kwargs):
        """Override save to set lineitem total and update order total"""
        self.lineitem_total = self.ticket.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.ticket.ticket_type} for {self.ticket.event.title} (x{self.quantity})'