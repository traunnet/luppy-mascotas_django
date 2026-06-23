from django.urls import path
from clienteApp.mascotas import views

urlpatterns = [
    path('',                        views.lista_mascotas,   name='lista_mascotas'),
    path('crear/',                  views.crear_mascota,    name='crear_mascota'),
    path('<int:pk>/editar/',        views.editar_mascota,   name='editar_mascota'),
    path('<int:pk>/eliminar/',      views.eliminar_mascota, name='eliminar_mascota'),
    path('<int:id_mascota>/historial/', views.historial_clinico, name='historial_clinico'),
    path('api/razas/',              views.obtener_razas,    name='obtener_razas'),
]