from django.db import models

class TipoServicio(models.Model):
    tipo = models.CharField(max_length=60)
    descripcion = models.CharField(max_length=250, blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    duracion = models.TimeField()
    imagen = models.ImageField(upload_to='servicios/', blank=True, null=True)

    class Meta:
        verbose_name = 'Tipo de Servicio'
        verbose_name_plural = 'Tipos de Servicios'
        db_table = 'tipo_servicio'

    def __str__(self):
        return self.tipo