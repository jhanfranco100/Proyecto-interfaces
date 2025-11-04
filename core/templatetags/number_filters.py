from django import template
import locale
from decimal import Decimal, InvalidOperation

register = template.Library()

@register.filter(name='format_price')
def format_price(value):
    if value is None or value == '':
        return "No disponible"

    try:
        # Establecer la configuración regional para Colombia (español)
        locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')
    except locale.Error:
        # Si la configuración regional no está disponible, usar una por defecto
        locale.setlocale(locale.LC_ALL, '')

    price_str = str(value).replace(',', '')
    try:
        price = float(price_str)
        return locale.currency(price, grouping=True, symbol=True)
    except (ValueError, TypeError, InvalidOperation):
        return value
