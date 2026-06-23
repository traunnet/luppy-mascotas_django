from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Rol,Usuario, Cliente, Veterinario

@admin.register(Rol)
class RolAdmin(ImportExportModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Usuario)
class UsuarioAdmin(ImportExportModelAdmin):
    list_display = ('correo', 'nombre', 'apellido', 'rol')
    search_fields = ('correo', 'nombre', 'apellido')
    list_filter = ('rol',)

admin.site.register(Cliente)
admin.site.register(Veterinario)