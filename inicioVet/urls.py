from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name="inicio"),
    path('servicios/', views.inicioServ, name="inicioServ"),
    path('productos/', views.inicioProd, name="inicioProd")
]