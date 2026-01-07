from django.contrib import admin
from .models import Ticket, Order, OrderLineItem


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


class OrderLineItemInline(admin.TabularInline):
    """Inline admin for OrderLineItem"""
    model = OrderLineItem
    readonly_fields = ['lineitem_total']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin configuration for Order model"""
    inlines = [OrderLineItemInline]

    list_display = [
        'order_number',
        'full_name',
        'email',
        'date',
        'order_total',
    ]
    list_filter = ['date']
    search_fields = ['order_number', 'full_name', 'email']
    readonly_fields = ['order_number', 'date', 'order_total']

    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'date', 'user')
        }),
        ('Customer Details', {
            'fields': ('full_name', 'email', 'phone_number')
        }),
        ('Payment', {
            'fields': ('order_total', 'stripe_pid')
        }),
    )

    def has_add_permission(self, request):
        """Disable manual order creation in admin"""
        return False
