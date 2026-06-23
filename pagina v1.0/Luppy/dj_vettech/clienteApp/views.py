#importaciones necesarias para las vistas del cliente
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import FormularioCita
from .utils import enviar_correo_compra
from .models import (
    Mascota, TipoServicio, Cita, HistorialClinico, TipoProducto, Inventario, Venta, DetalleVenta
)
from loginVet.models import Cliente, Usuario
from loginVet.forms import PerfilForm
from .reciboC_pdf import generar_recibo_pdf
from .forms import FormularioMascota, RAZAS_POR_ESPECIE



def get_cliente(user):
    cliente, _ = Cliente.objects.get_or_create(usuario=user)
    return cliente

@login_required
def dashboard(request):
    cliente = get_cliente(request.user)
    mascotas = Mascota.objects.filter(id_cliente=cliente)
    citas_proximas = Cita.objects.filter(
        id_cliente=cliente,
        estado_cita='PROGRAMADA'
    ).order_by('fecha_cita')[:5]
    return render(request, 'clienteApp/dashboard.html', {
        'cliente': cliente,
        'mascotas': mascotas,
        'citas_proximas': citas_proximas,
    })

@login_required
def lista_productos(request):
    inventarios = Inventario.objects.select_related('id_tipo_producto').all()

    nombre = request.GET.get('nombre')
    categoria = request.GET.get('categoria')
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')
    disponible = request.GET.get('disponible')
    if nombre:
        inventarios = inventarios.filter(id_tipo_producto__nombre_producto__icontains=nombre)
    if categoria:
        inventarios = inventarios.filter(id_tipo_producto__categoria__icontains=categoria)
    if precio_min:
        inventarios = inventarios.filter(id_tipo_producto__precio_unitario__gte=precio_min)
    if precio_max:
        inventarios = inventarios.filter(id_tipo_producto__precio_unitario__lte=precio_max)
    if disponible == 'on':
        inventarios = inventarios.filter(cantidad__gt=0)
    return render(request, 'clienteApp/lista_productos.html', {'inventarios': inventarios})


@login_required
def ver_carrito(request):
    carrito, _ = Venta.objects.get_or_create(
        id_cliente=request.user.cliente,
        estado='CARRITO',
        defaults={'total': 0}
    )

    items = DetalleVenta.objects.filter(id_venta=carrito)

    total = sum(item.precio_unitario * item.cantidad for item in items)
    carrito.total = total
    carrito.save()

    return render(request, 'clienteApp/carrito.html', {
        'items': items,
        'total': total
    })


@login_required
def agregar_carrito(request, producto_id):
    producto = get_object_or_404(TipoProducto, pk=producto_id)
    inventario = Inventario.objects.filter(id_tipo_producto=producto).first()
    if not inventario:
        messages.error(request, 'Este producto no tiene inventario registrado.')
        return redirect('lista_productos')
    if inventario.cantidad <= 0:
        messages.error(request, 'Sin stock disponible.')
        return redirect('lista_productos')
    carrito, _ = Venta.objects.get_or_create(
        id_cliente=request.user.cliente,
        estado='CARRITO',
        defaults={'total': 0}
    )
    item, creado = DetalleVenta.objects.get_or_create(
        id_venta=carrito,
        id_inventario=inventario,
        defaults={
            'cantidad': 1,
            'precio_unitario': producto.precio_unitario
        }
    )
    if not creado:
        if item.cantidad + 1 > inventario.cantidad:
            messages.error(request, f'No puedes superar el stock disponible ({inventario.cantidad}).')
            return redirect('carrito')
        item.cantidad += 1
        item.save()
    messages.success(request, f'{producto.nombre_producto} agregado al carrito.')
    return redirect('carrito')


@login_required
def eliminar_carrito(request, item_id):
    item = get_object_or_404(DetalleVenta, pk=item_id, id_venta__id_cliente=request.user.cliente)
    item.delete()
    messages.success(request, 'Producto eliminado.')
    return redirect('carrito')


@login_required
def actualizar_carrito(request, item_id):
    item = get_object_or_404(
        DetalleVenta,
        pk=item_id,
        id_venta__id_cliente=request.user.cliente
    )
    if request.method == 'POST':
        try:
            cantidad = int(request.POST.get('cantidad', 1))
        except (TypeError, ValueError):
            messages.error(request, 'Cantidad inválida.')
            return redirect('carrito')
        stock = item.id_inventario.cantidad
        if cantidad < 1:
            item.delete()
            messages.success(request, 'Producto eliminado del carrito.')
        elif cantidad > stock:
            messages.error(request, f'No puedes superar el stock disponible ({stock}).')
        else:
            item.cantidad = cantidad
            item.save()
            messages.success(request, 'Carrito actualizado correctamente.')
    return redirect('carrito')

@login_required
def pagar(request):
    carrito = Venta.objects.filter(
        id_cliente=request.user.cliente,
        estado='CARRITO'
    ).first()
    if not carrito:
        messages.error(request, "No hay carrito activo.")
        return redirect('carrito')
    items = DetalleVenta.objects.filter(id_venta=carrito)
    total = 0
    for item in items:
        inventario = item.id_inventario
        if item.cantidad > inventario.cantidad:
            messages.error(request, f'Sin stock suficiente para {inventario.id_tipo_producto.nombre_producto}')
            return redirect('carrito')
        inventario.cantidad -= item.cantidad
        inventario.save()
        total += item.cantidad * item.precio_unitario
    carrito.total = total
    carrito.estado = 'COMPLETADO'
    carrito.save()
    enviar_correo_compra(request.user, carrito, items)
    messages.success(request, "Compra realizada con éxito")
    return generar_recibo_pdf(request.user, carrito, items)

@login_required
def descargar_recibo(request, venta_id):
    venta = get_object_or_404(Venta, pk=venta_id, id_cliente=request.user.cliente, estado='COMPLETADO')
    items = DetalleVenta.objects.filter(id_venta=venta)
    return generar_recibo_pdf(request.user, venta, items)

@login_required
def historial_compras(request):
    ventas = Venta.objects.filter(id_cliente=request.user.cliente).order_by('-fecha_venta')
    return render(request, 'clienteApp/historial_compras.html', {'ventas': ventas})


@login_required
def perfil_cliente(request):
    return render(request, 'clienteApp/perfil.html', {
        'usuario': request.user  # pasa explícitamente para mayor claridad
    })



@login_required
def actualizar_perfil(request):
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('perfil_cliente')
        else:
            messages.error(request, 'Corrija los errores del formulario.')
    else:
        form = PerfilForm(instance=request.user)
    return render(request, 'clienteApp/formulario_perfil.html', {
        'form': form,
        'usuario': request.user
    })

def obtener_razas(request):
    especie = request.GET.get('especie')
    razas = RAZAS_POR_ESPECIE.get(especie, [])
    return JsonResponse({'razas': razas})