from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Usuarios)
admin.site.register(Inventario)
admin.site.register(contacto)
admin.site.register(Venta)
admin.site.register(DetalleVenta)
admin.site.register(Insumo)
admin.site.register(MetodoPago)
admin.site.register(Notificacion)