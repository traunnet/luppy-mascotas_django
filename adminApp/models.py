from django.db import models
from clienteApp.models import Inventario, TipoProducto
from loginVet.models import Usuario

class EntradaProducto(models.Model):
    """Registro de entradas de stock al inventario"""
    id_inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE,related_name='entradas')
    cantidad = models.PositiveIntegerField()
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    proveedor = models.CharField(max_length=120, blank=True)
    observacion = models.TextField(blank=True)
    registrado_por = models.ForeignKey(Usuario, null=True,on_delete=models.SET_NULL)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'entrada_producto'
        verbose_name = 'Entrada de Producto'
        ordering = ['-fecha']

    def __str__(self):
        return f"Entrada {self.pk} - {self.id_inventario}"

class SalidaProducto(models.Model):
    """Registro de salidas manuales de stock (bajas, pérdidas, etc.)"""
    MOTIVO_CHOICES = [
        ('BAJA','Baja por vencimiento'),
        ('PERDIDA','Pérdida o robo'),
        ('DANO','Producto dañado'),
        ('OTRO','Otro'),
    ]
    id_inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE, related_name='salidas')
    cantidad = models.PositiveIntegerField()
    motivo = models.CharField(max_length=10, choices=MOTIVO_CHOICES, default='OTRO')
    observacion = models.TextField(blank=True)
    registrado_por = models.ForeignKey(Usuario, null=True, on_delete=models.SET_NULL)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'salida_producto'
        verbose_name = 'Salida de Producto'
        ordering = ['-fecha']

    def __str__(self):
        return f"Salida {self.pk} - {self.id_inventario}"