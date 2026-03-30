from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# --- MODELO ROL ---
class Rol(models.Model):
    nombre = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = 'rol'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.nombre


# --- MANAGER ---
class UsuarioManager(BaseUserManager):
    def create_user(self, correo, password=None, **extra_fields):
        if not correo:
            raise ValueError("El correo es obligatorio")

        # Buscamos un rol por defecto si no se proporciona uno
        if 'rol' not in extra_fields and 'rol_id' not in extra_fields:
            # Esto evita el error de "null" si no mandas el rol
            rol_default, _ = Rol.objects.get_or_create(nombre="Usuario")
            extra_fields['rol'] = rol_default

        correo = self.normalize_email(correo)
        user = self.model(correo=correo, **extra_fields)
        user.set_password(password) 
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        # Asignamos el rol de Administrador automáticamente
        rol_admin, _ = Rol.objects.get_or_create(nombre="Administrador")
        extra_fields['rol'] = rol_admin

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(correo, password, **extra_fields)


# --- MODELO USUARIO ---
class Usuario(AbstractBaseUser, PermissionsMixin):
    correo = models.EmailField(unique=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    
    # El campo que causaba el error
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre', 'apellido'] # Django te pedirá estos al crear superuser

    class Meta:
        db_table = 'usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.correo})"