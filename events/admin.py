from django.contrib import admin
from .models import Category, Event


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category model"""
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Admin configuration for Event model"""
    list_display = [
        'title',
        'category',
        'city',
        'event_date',
        'is_active',
        'created_at'
    ]
    list_filter = ['is_active', 'category', 'event_date', 'city', 'country']
    search_fields = ['title', 'description', 'venue', 'city']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'created_by']
    date_hierarchy = 'event_date'

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'description')
        }),
        ('Location', {
            'fields': ('venue', 'address', 'city', 'country')
        }),
        ('Event Details', {
            'fields': ('event_date', 'image', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """Automatically set created_by to the current user"""
        if not change:  # Only set on creation
            obj.created_by = request.user
        super().save_model(request, obj, form, change)