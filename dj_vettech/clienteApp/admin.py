from django.contrib import admin
from .models import (
    Mascota, TipoServicio, Cita,
    HistorialClinico, TipoProducto,
    Inventario, Venta, DetalleVenta
)

admin.site.register(Mascota)
admin.site.register(TipoServicio)
admin.site.register(Cita)
admin.site.register(HistorialClinico)
admin.site.register(TipoProducto)
admin.site.register(Inventario)
admin.site.register(Venta)
admin.site.register(DetalleVenta)