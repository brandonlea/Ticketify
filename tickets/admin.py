from django.contrib import admin
from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """Admin configuration for Ticket model"""
    list_display = [
        'event',
        'ticket_type',
        'price',
        'quantity_available',
        'quantity_sold',
        'quantity_remaining',
        'is_active',
    ]
    list_filter = ['ticket_type', 'is_active', 'event__category']
    search_fields = ['event__title', 'description']
    readonly_fields = ['created_at', 'quantity_remaining', 'percentage_sold']

    fieldsets = (
        ('Ticket Information', {
            'fields': ('event', 'ticket_type', 'description', 'price')
        }),
        ('Availability', {
            'fields': (
                'quantity_available',
                'quantity_sold',
                'quantity_remaining',
                'percentage_sold',
                'is_active'
            )
        }),
        ('Sale Period', {
            'fields': ('sale_start_date', 'sale_end_date'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def quantity_remaining(self, obj):
        """Display remaining tickets"""
        remaining = obj.quantity_remaining
        if remaining == 0:
            return f"SOLD OUT"
        elif remaining < 10:
            return f"{remaining} (Low Stock)"
        return remaining
    quantity_remaining.short_description = 'Remaining'

    def percentage_sold(self, obj):
        """Display percentage sold"""
        return f"{obj.percentage_sold:.1f}%"
    percentage_sold.short_description = '% Sold'
