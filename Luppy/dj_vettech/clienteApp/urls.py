from django.urls import path, include
from . import views
from . import citas_views

urlpatterns = [
    path('', views.dashboard, name='dashboard_cliente'),
    path('mascotas/', include('clienteApp.mascotas.urls')),

    path('citas/', citas_views.lista_citas, name='lista_citas'),
    path('citas/crear/', citas_views.crear_cita, name='crear_cita'),
    path('citas/<int:pk>/cancelar/', citas_views.eliminar_cita, name='cancelar_cita'),
    path('citas/<int:pk>/eliminar/', citas_views.eliminar_cita, name='eliminar_cita'),

    path('productos/', views.lista_productos, name='lista_productos'),
    path('carrito/', views.ver_carrito, name='carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_carrito, name='eliminar_carrito'),
    path('carrito/actualizar/<int:item_id>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('pagar/', views.pagar, name='pagar'),
    path('compras/', views.historial_compras, name='historial_compras'),
    path('perfil/', views.perfil_cliente, name='perfil_cliente'),
    path('perfil/actualizar/', views.actualizar_perfil, name='actualizar_perfil'),
    path('recibo/<int:venta_id>/', views.descargar_recibo, name='descargar_recibo'),
]