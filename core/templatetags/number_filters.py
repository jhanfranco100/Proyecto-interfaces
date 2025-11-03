from django import template
import locale

register = template.Library()

@register.filter(name='format_price')
def format_price(value):
    if value is None:
        return "No disponible"

    try:
        # Intentar convertir el valor a un número flotante
        price = float(value)
        # Formatear el número con separadores de miles y dos decimales
        return f'{price:,.2f}'.replace(',', 'temp').replace('.', ',').replace('temp', '.')
    except (ValueError, TypeError):
        # Si el valor no es un número válido, devolver el valor original
        return value
