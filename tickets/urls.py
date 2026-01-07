from django.urls import path
from . import views

app_name = 'tickets'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('payment-success/<str:order_number>/', views.payment_success, name='payment_success'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
]