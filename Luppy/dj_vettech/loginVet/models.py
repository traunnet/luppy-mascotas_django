from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class Rol(models.Model):
    NOMBRES_CHOICES = [
        ('ADMINISTRADOR', 'Administrador'),
        ('VETERINARIO', 'Veterinario'),
        ('CLIENTE', 'Cliente'),
    ]
    nombre = models.CharField(max_length=20, choices=NOMBRES_CHOICES, unique=True)
    descripcion = models.CharField(max_length=150, blank=True)

    class Meta:
        db_table = 'rol'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.nombre

class UsuarioManager(BaseUserManager):
    def create_user(self, correo, password=None, **extra_fields):
        if not correo:
            raise ValueError("El correo es obligatorio")
        if 'rol' not in extra_fields and 'rol_id' not in extra_fields:
            rol_default, _ = Rol.objects.get_or_create(nombre='CLIENTE')
            extra_fields['rol'] = rol_default
        correo = self.normalize_email(correo)
        user = self.model(correo=correo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        rol_admin, _ = Rol.objects.get_or_create(nombre='ADMINISTRADOR')
        extra_fields['rol'] = rol_admin
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')
        return self.create_user(correo, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    TIPO_DOC_CHOICES = [
        ('TI', 'Tarjeta de Identidad'),
        ('CC', 'Cédula de Ciudadanía'),
        ('CE', 'Cédula de Extranjería'),
        ('NIT', 'NIT'),
    ]

    tipo_doc = models.CharField(max_length=3, choices=TIPO_DOC_CHOICES, default='CC')
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=10, unique=True, blank=True, null=True)
    direccion = models.CharField(max_length=150, blank=True)
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    numero_documento = models.CharField(max_length=20, unique=True, null=True, blank=True)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre', 'apellido']
    
    @property
    def email(self):
        return self.correo

    @email.setter
    def email(self, value):
        self.correo = value
    class Meta:
        db_table = 'usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.correo})"

class Cliente(models.Model):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column='id_cliente',
        related_name='cliente'
    )
    fecha_registro = models.DateField(null=True, blank=True)
    mascotas_registradas = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'cliente'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return str(self.usuario)

class Veterinario(models.Model):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column='id_veterinario',
        related_name='veterinario'
    )
    numero_licencia = models.CharField(max_length=30, unique=True)
    especialidad = models.CharField(max_length=80, blank=True)
    anios_experiencia = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        db_table = 'veterinario'
        verbose_name = 'Veterinario'
        verbose_name_plural = 'Veterinarios'

    def __str__(self):
        return str(self.usuario)