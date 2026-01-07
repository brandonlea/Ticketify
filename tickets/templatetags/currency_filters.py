from django import template
from decimal import Decimal

register = template.Library()


@register.filter(name='currency')
def currency(value):
    """
    Format a number as currency with thousand separators
    Example: 24000.00 -> 24,000.00
    """
    try:
        # Convert to Decimal if not already
        if not isinstance(value, Decimal):
            value = Decimal(str(value))

        # Format with 2 decimal places and thousand separators
        return "{:,.2f}".format(value)
    except (ValueError, TypeError, AttributeError):
        return value