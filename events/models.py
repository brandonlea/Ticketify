from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils import timezone


class Category(models.Model):
    """
    Category model for organizing events into different types
    (e.g., Music, Sports, Theater, Conference)
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        """Auto-generate slug from name if not provided"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Event(models.Model):
    """
    Event model representing an event that users can purchase tickets for
    """
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events'
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    venue = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='Ireland')
    event_date = models.DateTimeField()
    capacity = models.PositiveIntegerField(
        default=1000,
        help_text='Maximum venue capacity for this event'
    )
    image = models.ImageField(
        upload_to='events/',
        null=True,
        blank=True,
        default='events/placeholder.jpg'
    )
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_events'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['event_date']
        indexes = [
            models.Index(fields=['event_date', 'is_active']),
            models.Index(fields=['slug']),
        ]

    def save(self, *args, **kwargs):
        """Auto-generate slug from title if not provided"""
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            # Ensure slug is unique
            while Event.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def clean(self):
        """Validate that event_date is in the future"""
        if self.event_date and self.event_date < timezone.now():
            raise ValidationError({
                'event_date': 'Event date must be in the future.'
            })

    def __str__(self):
        return f"{self.title} - {self.event_date.strftime('%d %b %Y')}"

    def get_absolute_url(self):
        """Return the URL for this event"""
        from django.urls import reverse
        return reverse('events:event_detail', kwargs={'slug': self.slug})

    @property
    def is_past(self):
        """Check if the event has already occurred"""
        return self.event_date < timezone.now()

    @property
    def total_tickets_sold(self):
        """Calculate total tickets sold across all ticket types"""
        return sum(
            ticket.quantity_sold
            for ticket in self.tickets.all()
        )

    @property
    def total_tickets_available(self):
        """Calculate total tickets still available across all ticket types"""
        return sum(
            ticket.quantity_remaining
            for ticket in self.tickets.filter(is_active=True)
        )

    @property
    def has_available_tickets(self):
        """Check if event has any tickets available for purchase"""
        return self.total_tickets_available > 0

    @property
    def capacity_percentage(self):
        """Calculate percentage of venue capacity sold"""
        if self.capacity == 0:
            return 0
        return (self.total_tickets_sold / self.capacity) * 100

    @property
    def is_at_capacity(self):
        """Check if event has reached venue capacity"""
        return self.total_tickets_sold >= self.capacity

    @property
    def min_price(self):
        """Get the minimum ticket price for this event"""
        tickets = self.tickets.filter(is_active=True)
        if tickets.exists():
            return min(ticket.price for ticket in tickets)
        return None