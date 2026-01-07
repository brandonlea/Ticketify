"""
URL configuration for Ticketify project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from events import views as event_views
from events import error_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', event_views.home, name='home'),
    path('events/', include('events.urls')),
    path('accounts/', include('accounts.urls')),
    path('cart/', include('cart.urls')),
    path('tickets/', include('tickets.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Test URLs for error pages (only in DEBUG mode)
    urlpatterns += [
        path('test-404/', error_views.custom_404, name='test_404'),
        path('test-500/', error_views.custom_500, name='test_500'),
        path('test-403/', error_views.custom_403, name='test_403'),
        path('test-400/', error_views.custom_400, name='test_400'),
    ]

# Custom error handlers
handler404 = 'events.error_views.custom_404'
handler500 = 'events.error_views.custom_500'
handler403 = 'events.error_views.custom_403'
handler400 = 'events.error_views.custom_400'
