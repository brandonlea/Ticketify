from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.utils import timezone
from .models import Event, Category


class EventListView(ListView):
    """View for listing all active events"""
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 12

    def get_queryset(self):
        """Filter active events and allow search/filter"""
        queryset = Event.objects.filter(
            is_active=True,
            event_date__gte=timezone.now()
        ).select_related('category')

        # Search functionality
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(city__icontains=search_query) |
                Q(venue__icontains=search_query)
            )

        # Category filter
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # City filter
        city = self.request.GET.get('city')
        if city:
            queryset = queryset.filter(city__iexact=city)

        return queryset

    def get_context_data(self, **kwargs):
        """Add extra context"""
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['search_query'] = self.request.GET.get('q', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_city'] = self.request.GET.get('city', '')

        # Get unique cities for filter
        context['cities'] = Event.objects.filter(
            is_active=True
        ).values_list('city', flat=True).distinct().order_by('city')

        return context


class EventDetailView(DetailView):
    """View for displaying event details"""
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

    def get_queryset(self):
        """Only show active events"""
        return Event.objects.filter(is_active=True).select_related('category')

    def get_context_data(self, **kwargs):
        """Add tickets to context"""
        context = super().get_context_data(**kwargs)
        context['tickets'] = self.object.tickets.filter(
            is_active=True
        ).order_by('price')
        return context


def home(request):
    """Home page view"""
    featured_events = Event.objects.filter(
        is_active=True,
        event_date__gte=timezone.now()
    ).select_related('category').order_by('event_date')[:6]

    categories = Category.objects.all()

    context = {
        'featured_events': featured_events,
        'categories': categories,
    }
    return render(request, 'home.html', context)