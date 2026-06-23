from django.urls import path
from . import views
from . import exportar_excel, exportar_pdf
app_name = 'vet_app'

urlpatterns = [
    path('', views.vet_dashboard, name='dashboard'),
    path('agenda/', views.AgendaCitasView.as_view(), name='agenda_citas'),
    path('gestion/', views.GestionCitasView.as_view(), name='gestion_citas'),
    path('gestion/crear/', views.CrearCitaView.as_view(), name='crear_cita'),
    path('gestion/<int:pk>/actualizar/', views.ActualizarCitaView.as_view(), name='actualizar_cita'),
    path('gestion/<int:pk>/eliminar/', views.EliminarCitaView.as_view(), name='eliminar_cita'),
    path('ajax/mascotas/<int:cliente_id>/', views.get_mascotas_por_cliente, name='mascotas_por_cliente'),
    path('ajax/citas/<int:mascota_id>/', views.get_citas_por_mascota, name='citas_por_mascota'),
    path('historial/', views.HistorialClinicoView.as_view(), name='historial_clinico'),
    path('historial/crear/', views.CrearHistorialView.as_view(), name='crear_historial'),
    path('historial/<int:pk>/actualizar/', views.ActualizarHistorialView.as_view(), name='actualizar_historial'),
    path('inventario/', views.InventarioListView.as_view(), name='lista_inventario'),
    path('inventario/producto/crear/', views.CrearProductoView.as_view(), name='crear_producto'),
    path('inventario/producto/<int:pk>/editar/', views.ActualizarProductoView.as_view(), name='editar_producto'),
    path('inventario/producto/<int:pk>/eliminar/', views.EliminarProductoView.as_view(), name='eliminar_producto'),
    path('inventario/entrada/', views.CrearEntradaProductoView.as_view(), name='crear_entrada'),
    path('inventario/salida/', views.CrearSalidaProductoView.as_view(), name='crear_salida'),
    path('ventas/', views.VentaListView.as_view(), name='ventas'),
    path('ventas/crear/', views.CrearVentaView.as_view(), name='crear_venta'),
    path('reportes/', views.ReporteGeneralView.as_view(), name='reportes'),
    path('reportes/excel/', exportar_excel.exportar_excel, name='exportar_excel'),
    path('reportes/pdf/', exportar_pdf.exportar_pdf, name='exportar_pdf'),
    path('perfil/', views.PerfilView.as_view(), name='perfil'),
    path('perfil/actualizar/', views.ActualizarPerfilView.as_view(), name='actualizar_perfil'),
]