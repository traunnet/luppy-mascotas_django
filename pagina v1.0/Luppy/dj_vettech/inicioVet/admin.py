from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import TipoServicio

@admin.register(TipoServicio)
class TipoServicioAdmin(ImportExportModelAdmin):
    list_display = ('tipo', 'precio', 'duracion')
    search_fields = ('tipo',)
    list_filter = ('precio',)
