from django.db import models
from loginVet.models import Cliente, Veterinario


# --- MODELO MASCOTA ---
class Mascota(models.Model):
    SEXO_CHOICES = [('HEMBRA', 'Hembra'), ('MACHO', 'Macho')]

    nombre = models.CharField(max_length=50)
    edad = models.PositiveSmallIntegerField(null=True, blank=True)
    especie = models.CharField(max_length=40)
    sexo = models.CharField(max_length=6, choices=SEXO_CHOICES)
    raza = models.CharField(max_length=50)
    color = models.CharField(max_length=30, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    cantidad_visitas = models.PositiveSmallIntegerField(default=0)
    estado = models.CharField(max_length=50, default='Activo')
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column='id_cliente')

    class Meta:
        db_table = 'mascota'
        verbose_name = 'Mascota'
        verbose_name_plural = 'Mascotas'

    def __str__(self):
        return self.nombre


# --- MODELO TIPO SERVICIO ---
class TipoServicio(models.Model):
    tipo = models.CharField(max_length=60)
    descripcion = models.CharField(max_length=250, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='servicios/', blank=True, null=True)
    duracion = models.TimeField()
    creado_el = models.DateTimeField(auto_now_add=True)
    actualizado_el = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tipo_servicio_cliente'
        verbose_name = 'Tipo de Servicio'
        verbose_name_plural = 'Tipos de Servicio'

    def __str__(self):
        return self.tipo


# --- MODELO CITA ---
class Cita(models.Model):
    ESTADO_CHOICES = [
        ('PROGRAMADA', 'Programada'),
        ('COMPLETADA', 'Completada'),
        ('CANCELADA', 'Cancelada'),
    ]

    id_cliente = models.ForeignKey(Cliente, null=True, on_delete=models.SET_NULL, db_column='id_cliente')
    id_mascota = models.ForeignKey(Mascota, null=True, on_delete=models.CASCADE, db_column='id_mascota')
    id_veterinario = models.ForeignKey(Veterinario, on_delete=models.RESTRICT, db_column='id_veterinario')
    id_servicio = models.ForeignKey(TipoServicio, null=True, on_delete=models.SET_NULL, db_column='id_servicio')
    fecha_cita = models.DateField()
    hora_cita = models.TimeField()
    estado_cita = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='PROGRAMADA')
    motivo = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cita'
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'

    def __str__(self):
        return f"Cita {self.pk} - {self.fecha_cita}"


# --- MODELO HISTORIAL CLINICO ---
class HistorialClinico(models.Model):
    fecha = models.DateField()
    motivo_consulta = models.CharField(max_length=255, blank=True)
    diagnostico = models.TextField()
    tratamiento = models.TextField(blank=True)
    medicacion = models.CharField(max_length=150, blank=True)
    frecuencia = models.CharField(max_length=80, blank=True)
    estado = models.CharField(max_length=50, blank=True)
    id_mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, db_column='id_mascota')
    id_servicio = models.ForeignKey(TipoServicio, null=True, on_delete=models.SET_NULL, db_column='id_servicio')
    id_veterinario = models.ForeignKey(Veterinario, null=True, on_delete=models.SET_NULL, db_column='id_veterinario')
    id_cita = models.ForeignKey(Cita, null=True, on_delete=models.SET_NULL, db_column='id_cita')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'historial_clinico'
        verbose_name = 'Historial Clínico'
        verbose_name_plural = 'Historiales Clínicos'

    def __str__(self):
        return f"Historial {self.pk} - {self.id_mascota.nombre}"


# --- MODELO TIPO PRODUCTO ---
class TipoProducto(models.Model):
    nombre_producto = models.CharField(max_length=120)
    categoria = models.CharField(max_length=60)
    descripcion = models.TextField(blank=True)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    class Meta:
        db_table = 'tipo_producto'
        verbose_name = 'Tipo de Producto'
        verbose_name_plural = 'Tipos de Producto'

    def __str__(self):
        return self.nombre_producto


# --- MODELO INVENTARIO ---
class Inventario(models.Model):
    id_tipo_producto = models.ForeignKey(TipoProducto, on_delete=models.CASCADE, db_column='id_tipo_producto')
    cantidad = models.PositiveIntegerField(default=0)
    ubicacion = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'inventario'
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'

    def __str__(self):
        return f"{self.id_tipo_producto.nombre_producto} - {self.cantidad} unidades"


# --- MODELO VENTA ---
class Venta(models.Model):
    ESTADO_CHOICES = [
        ('CARRITO', 'Carrito'),
        ('COMPLETADO', 'Completado'),
    ]

    id_vet = models.ForeignKey(Veterinario, null=True, on_delete=models.SET_NULL, db_column='id_vet')
    id_cliente = models.ForeignKey(Cliente, null=True, on_delete=models.SET_NULL, db_column='id_cliente')
    fecha_venta = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='CARRITO')

    class Meta:
        db_table = 'ventas' 


# --- MODELO DETALLE VENTA ---
class DetalleVenta(models.Model):
    id_venta = models.ForeignKey(Venta, on_delete=models.CASCADE, db_column='id_venta')
    id_inventario = models.ForeignKey(Inventario, on_delete=models.RESTRICT, db_column='id_inventario')
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'detalle_venta'
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalles de Venta'

    def __str__(self):
        return f"Detalle {self.pk} - Venta {self.id_venta.pk}"