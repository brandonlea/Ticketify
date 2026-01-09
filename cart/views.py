from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from tickets.models import Ticket
from .cart import Cart


def cart_detail(request):
    """
    Display the cart
    """
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


@require_POST
def cart_add(request, ticket_id):
    """
    Add a ticket to the cart
    """
    cart = Cart(request)
    ticket = get_object_or_404(Ticket, id=ticket_id)
    quantity = int(request.POST.get('quantity', 1))

    # Check if ticket is available
    if not ticket.is_available:
        messages.error(request, f'{ticket.event.title} - {ticket.get_ticket_type_display()} is sold out.')
        return redirect('events:event_detail', slug=ticket.event.slug)

    # Check if there are enough tickets available
    if quantity > ticket.quantity_remaining:
        messages.error(
            request,
            f'Only {ticket.quantity_remaining} tickets available for {ticket.event.title} - {ticket.get_ticket_type_display()}.'
        )
        return redirect('events:event_detail', slug=ticket.event.slug)

    cart.add(ticket=ticket, quantity=quantity)
    messages.success(request, f'Added {quantity} x {ticket.get_ticket_type_display()} ticket(s) to your cart.')
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, ticket_id):
    """
    Remove a ticket from the cart
    """
    cart = Cart(request)
    ticket = get_object_or_404(Ticket, id=ticket_id)
    cart.remove(ticket)
    messages.success(request, 'Item removed from cart.')
    return redirect('cart:cart_detail')


@require_POST
def cart_update(request, ticket_id):
    """
    Update the quantity of a ticket in the cart
    """
    cart = Cart(request)
    ticket = get_object_or_404(Ticket, id=ticket_id)
    quantity = int(request.POST.get('quantity', 1))

    # Check if there are enough tickets available
    if quantity > ticket.quantity_remaining:
        messages.error(
            request,
            f'Only {ticket.quantity_remaining} tickets available for {ticket.event.title} - {ticket.get_ticket_type_display()}.'
        )
        return redirect('cart:cart_detail')

    cart.update_quantity(ticket=ticket, quantity=quantity)
    messages.success(request, 'Cart updated.')
    return redirect('cart:cart_detail')
