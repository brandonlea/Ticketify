from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin configuration for UserProfile model"""
    list_display = [
        'user',
        'phone_number',
        'town_or_city',
        'country',
    ]
    search_fields = ['user__username', 'user__email', 'phone_number']
    list_filter = ['country', 'town_or_city']

    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Contact Information', {
            'fields': ('phone_number',)
        }),
        ('Address', {
            'fields': (
                'street_address1',
                'street_address2',
                'town_or_city',
                'county',
                'postcode',
                'country'
            )
        }),
    )
