from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from cart.cart import Cart
from .models import Order, OrderLineItem, Ticket
import stripe
import uuid

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def checkout(request):
    """
    Display the checkout page
    """
    cart = Cart(request)

    if len(cart) == 0:
        messages.error(request, 'Your cart is empty.')
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        # Create order
        order = Order.objects.create(
            user=request.user,
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            country=request.POST.get('country'),
        )

        # Create order line items
        for item in cart:
            OrderLineItem.objects.create(
                order=order,
                ticket=item['ticket'],
                price=item['price'],
                quantity=item['quantity']
            )

        # Create Stripe payment intent
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(order.order_total * 100),
                currency='eur',
                metadata={
                    'order_id': str(order.id),
                    'order_number': order.order_number,
                }
            )

            order.stripe_pid = intent.id
            order.save()

            return render(request, 'tickets/payment.html', {
                'order': order,
                'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
                'client_secret': intent.client_secret,
            })

        except Exception as e:
            messages.error(request, f'Payment error: {str(e)}')
            order.delete()
            return redirect('cart:cart_detail')

    return render(request, 'tickets/checkout.html', {
        'cart': cart,
    })


@login_required
def payment_success(request, order_number):
    """
    Handle successful payment
    """
    order = get_object_or_404(Order, order_number=order_number, user=request.user)

    if order.paid:
        # Update ticket quantities
        for item in order.lineitems.all():
            ticket = item.ticket
            ticket.quantity_sold += item.quantity
            ticket.save()

        # Clear the cart
        cart = Cart(request)
        cart.clear()

        messages.success(request, f'Order {order.order_number} completed successfully!')
        return render(request, 'tickets/payment_success.html', {'order': order})
    else:
        messages.error(request, 'Payment not confirmed.')
        return redirect('cart:cart_detail')


@csrf_exempt
@require_POST
def stripe_webhook(request):
    """
    Handle Stripe webhooks
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        order_id = payment_intent['metadata'].get('order_id')

        try:
            order = Order.objects.get(id=order_id)
            order.paid = True
            order.save()

            # Update ticket quantities
            for item in order.lineitems.all():
                ticket = item.ticket
                ticket.quantity_sold += item.quantity
                ticket.save()

        except Order.DoesNotExist:
            pass

    return HttpResponse(status=200)