from django.urls import path
from . import views

app_name = 'admin_app'

urlpatterns = [

    # ── Dashboard principal ──────────────────────────────────────────
    path('', views.admin_dashboard, name='dashboard'),

    # ── Usuarios ────────────────────────────────────────────────────
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/<int:pk>/editar/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/<int:pk>/toggle/', views.toggle_usuario, name='toggle_usuario'),

    # ── Veterinarios ────────────────────────────────────────────────
    path('veterinarios/', views.lista_veterinarios, name='lista_veterinarios'),
    path('veterinarios/crear/', views.crear_veterinario, name='crear_veterinario'),
    path('veterinarios/<int:pk>/editar/', views.editar_veterinario, name='editar_veterinario'),

    # ── Citas ───────────────────────────────────────────────────────
    path('citas/', views.lista_citas_admin, name='lista_citas'),
    path('citas/<int:pk>/estado/', views.cambiar_estado_cita, name='cambiar_estado_cita'),

    # ── Inventario ──────────────────────────────────────────────────
    path('inventario/', views.lista_inventario, name='lista_inventario'),
    path('inventario/producto/crear/', views.crear_producto, name='crear_producto'),
    path('inventario/producto/<int:pk>/editar/', views.editar_producto, name='editar_producto'),
    path('inventario/producto/<int:pk>/eliminar/', views.eliminar_producto, name='eliminar_producto'),
    path('inventario/entrada/', views.registrar_entrada, name='registrar_entrada'),
    path('inventario/salida/', views.registrar_salida, name='registrar_salida'),

    # ── Servicios ───────────────────────────────────────────────────
    path('servicios/', views.lista_servicios, name='lista_servicios'),
    path('servicios/crear/', views.crear_servicio, name='crear_servicio'),
    path('servicios/<int:pk>/editar/', views.editar_servicio, name='editar_servicio'),
    path('servicios/<int:pk>/eliminar/', views.eliminar_servicio, name='eliminar_servicio'),

    # ── Reportes ────────────────────────────────────────────────────
    path('reportes/', views.reportes, name='reportes'),
    path('reportes/ventas/pdf/', views.reporte_ventas_pdf, name='reporte_ventas_pdf'),
    path('reportes/clientes/pdf/', views.reporte_clientes_pdf, name='reporte_clientes_pdf'),
    path('reportes/veterinarios/pdf/', views.reporte_veterinarios_pdf, name='reporte_veterinarios_pdf'),
]