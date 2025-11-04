from django.contrib import admin
from .models import *
from django.db.models.functions import Cast
from django.db.models import CharField

class InventarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'sub_categoria', 'precio_str_display')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            precio_str=Cast('precio', CharField())
        )

    def precio_str_display(self, obj):
        from .templatetags.number_filters import format_price
        return format_price(obj.precio_str)
    precio_str_display.short_description = 'Precio'

# Register your models here.
admin.site.register(Usuarios)
admin.site.register(Inventario, InventarioAdmin)
admin.site.register(contacto)
admin.site.register(Venta)
admin.site.register(DetalleVenta)
admin.site.register(Insumo)
admin.site.register(MetodoPago)
admin.site.register(Notificacion)