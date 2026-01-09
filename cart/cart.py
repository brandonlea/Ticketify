from decimal import Decimal
from tickets.models import Ticket


class Cart:
    def __init__(self, request):
        """
        Initialize the cart
        """
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, ticket, quantity=1):
        """
        Add a ticket to the cart or update its quantity
        """
        ticket_id = str(ticket.id)
        if ticket_id not in self.cart:
            self.cart[ticket_id] = {
                'quantity': 0,
                'price': str(ticket.price)
            }
        self.cart[ticket_id]['quantity'] += quantity
        self.save()

    def save(self):
        """
        Mark the session as modified to make sure it gets saved
        """
        self.session.modified = True

    def remove(self, ticket):
        """
        Remove a ticket from the cart
        """
        ticket_id = str(ticket.id)
        if ticket_id in self.cart:
            del self.cart[ticket_id]
            self.save()

    def update_quantity(self, ticket, quantity):
        """
        Update the quantity of a ticket
        """
        ticket_id = str(ticket.id)
        if ticket_id in self.cart:
            if quantity > 0:
                self.cart[ticket_id]['quantity'] = quantity
            else:
                self.remove(ticket)
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the tickets from the database
        """
        ticket_ids = self.cart.keys()
        tickets = Ticket.objects.filter(id__in=ticket_ids)
        cart = self.cart.copy()

        for ticket in tickets:
            cart[str(ticket.id)]['ticket'] = ticket

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Calculate the total price of all items in the cart
        """
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def clear(self):
        """
        Remove cart from session
        """
        del self.session['cart']
        self.save()
