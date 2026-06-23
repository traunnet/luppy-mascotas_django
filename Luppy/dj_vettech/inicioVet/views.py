from django.shortcuts import render
from clienteApp.models import TipoProducto
# Importa el modelo de servicios desde la app de cliente
# Ajusta la ruta si tu app tiene otro nombre
try:
    from clienteApp.models import TipoServicio
except ImportError:
    TipoServicio = None


def inicio(request):
    """
    Vista principal. Pasa al template:
      - total_servicios: conteo de servicios activos (para el stat del hero)
    """
    context = {}

    if TipoServicio is not None:
        context['total_servicios'] = TipoServicio.objects.count()
    else:
        context['total_servicios'] = 0

    return render(request, 'inicio.html', context)


def inicioServ(request):
    """
    Vista de catálogo de servicios.
    Pasa todos los TipoServicio ordenados por tipo.
    """
    context = {}

    if TipoServicio is not None:
        context['servs'] = TipoServicio.objects.all().order_by('tipo')
    else:
        context['servs'] = []

    return render(request, 'inicioServ.html', context)

def inicioProd(request):
    """
    Vista de catálogo de productos.
    Muestra una selección aleatoria de productos.
    """
    prods = TipoProducto.objects.order_by('?')[:6]  

    return render(request, 'inicioProd.html', {
        'prods': prods
    })