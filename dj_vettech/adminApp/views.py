from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from django.http import HttpResponse, FileResponse
import datetime
from io import BytesIO

from loginVet.models import Usuario, Rol, Veterinario, Cliente
from clienteApp.models import (
    Mascota, TipoServicio, Cita, TipoProducto, Inventario, Venta, DetalleVenta
)
from .models import EntradaProducto, SalidaProducto
from .forms import (
    FormularioUsuario, FormularioVeterinario, FormularioProducto,
    FormularioEntrada, FormularioSalida, FormularioServicio,
    FiltroReporteVentas, FiltroReporteCitas,
)

def es_admin(user):
    return user.is_authenticated and user.rol.nombre == 'ADMINISTRADOR'

admin_required = user_passes_test(es_admin, login_url='auth_app:login')

@login_required
@admin_required
def admin_dashboard(request):
    hoy = timezone.now().date()
    total_usuarios = Usuario.objects.count()
    total_clientes = Cliente.objects.count()
    total_vets = Veterinario.objects.count()
    total_mascotas = Mascota.objects.count()

    citas_programadas = Cita.objects.filter(estado_cita='PROGRAMADA').count()
    citas_completadas = Cita.objects.filter(estado_cita='COMPLETADA').count()
    citas_canceladas = Cita.objects.filter(estado_cita='CANCELADA').count()
    citas_hoy = Cita.objects.filter(fecha_cita=hoy).count()

    ingresos_ventas = Venta.objects.filter(estado='COMPLETADO').aggregate(total=Sum('total'))['total'] or 0
    ingresos_servicios = Cita.objects.filter(estado_cita='COMPLETADA').select_related('id_servicio').aggregate(total=Sum('id_servicio__precio'))['total'] or 0
    ingresos_totales = ingresos_ventas + ingresos_servicios

    UMBRAL_STOCK = 5
    productos_bajo_stock = Inventario.objects.filter(cantidad__lte=UMBRAL_STOCK).select_related('id_tipo_producto')
    ultimas_ventas = Venta.objects.filter(estado='COMPLETADO').order_by('-fecha_venta')[:5]
    proximas_citas = Cita.objects.filter(fecha_cita__gte=hoy, estado_cita='PROGRAMADA').select_related('id_mascota', 'id_veterinario__usuario').order_by('fecha_cita')[:5]

    grafico_citas = {
        'labels': ['Programadas', 'Completadas', 'Canceladas'],
        'valores': [citas_programadas, citas_completadas, citas_canceladas],
    }

    labels_ventas, valores_ventas = [], []
    for i in range(6, -1, -1):
        dia = hoy - datetime.timedelta(days=i)
        total_dia = Venta.objects.filter(fecha_venta__date=dia, estado='COMPLETADO').aggregate(t=Sum('total'))['t'] or 0
        labels_ventas.append(dia.strftime('%d/%m'))
        valores_ventas.append(float(total_dia))

    return render(request, 'adminApp/dashboard.html', {
        'total_usuarios': total_usuarios,
        'total_clientes': total_clientes,
        'total_vets': total_vets,
        'total_mascotas': total_mascotas,
        'citas_programadas': citas_programadas,
        'citas_completadas': citas_completadas,
        'citas_canceladas': citas_canceladas,
        'citas_hoy': citas_hoy,
        'ingresos_totales': ingresos_totales,
        'ingresos_ventas': ingresos_ventas,
        'ingresos_servicios': ingresos_servicios,
        'productos_bajo_stock': productos_bajo_stock,
        'ultimas_ventas': ultimas_ventas,
        'proximas_citas': proximas_citas,
        'grafico_citas': grafico_citas,
        'labels_ventas': labels_ventas,
        'valores_ventas': valores_ventas,
        'UMBRAL_STOCK': UMBRAL_STOCK,
    })

@login_required
@admin_required
def lista_usuarios(request):
    rol_filtro = request.GET.get('rol', '')
    busqueda = request.GET.get('q', '')
    usuarios = Usuario.objects.select_related('rol').all()

    if rol_filtro:
        usuarios = usuarios.filter(rol__nombre=rol_filtro)
    if busqueda:
        usuarios = usuarios.filter(
            Q(nombre__icontains=busqueda) | Q(apellido__icontains=busqueda) | Q(correo__icontains=busqueda)
        )
    roles = Rol.objects.all()
    return render(request, 'adminApp/usuarios/lista.html', {
        'usuarios': usuarios,
        'roles': roles,
        'rol_filtro': rol_filtro,
        'busqueda': busqueda,
    })

@login_required
@admin_required
def crear_usuario(request):
    if request.method == 'POST':
        form = FormularioUsuario(request.POST)
        if form.is_valid():
            usuario = form.save()
            if usuario.rol.nombre == 'VETERINARIO':
                Veterinario.objects.get_or_create(
                    usuario=usuario,
                    defaults={'numero_licencia': f'LIC-{usuario.pk}'}
                )
            elif usuario.rol.nombre == 'CLIENTE':
                Cliente.objects.get_or_create(
                    usuario=usuario,
                    defaults={'fecha_registro': timezone.now().date()}
                )
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('admin_app:lista_usuarios')
    else:
        form = FormularioUsuario()
    return render(request, 'adminApp/usuarios/formulario.html', {'form': form, 'titulo': 'Crear Usuario'})

@login_required
@admin_required
def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = FormularioUsuario(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado.')
            return redirect('admin_app:lista_usuarios')
    else:
        form = FormularioUsuario(instance=usuario)
    return render(request, 'adminApp/usuarios/formulario.html', {'form': form, 'titulo': 'Editar Usuario', 'usuario': usuario})

@login_required
@admin_required
def toggle_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if usuario == request.user:
        messages.error(request, 'No puedes desactivar tu propia cuenta.')
        return redirect('admin_app:lista_usuarios')
    usuario.is_active = not usuario.is_active
    usuario.save()
    estado = 'activado' if usuario.is_active else 'desactivado'
    messages.success(request, f'Usuario {estado} correctamente.')
    return redirect('admin_app:lista_usuarios')

@login_required
@admin_required
def lista_veterinarios(request):
    veterinarios = Veterinario.objects.select_related('usuario').all()
    return render(request, 'adminApp/veterinarios/lista.html', {'veterinarios': veterinarios})

@login_required
@admin_required
def crear_veterinario(request):
    form_usuario = FormularioUsuario(request.POST or None)
    form_vet = FormularioVeterinario(request.POST or None)
    if request.method == 'POST':
        if form_usuario.is_valid() and form_vet.is_valid():
            rol_vet, _ = Rol.objects.get_or_create(nombre='VETERINARIO')
            usuario = form_usuario.save(commit=False)
            usuario.rol = rol_vet
            usuario.save()
            vet = form_vet.save(commit=False)
            vet.usuario = usuario
            vet.save()
            messages.success(request, 'Veterinario registrado exitosamente.')
            return redirect('admin_app:lista_veterinarios')
    return render(request, 'adminApp/veterinarios/formulario.html', {'form_usuario': form_usuario, 'form_vet': form_vet, 'titulo': 'Registrar Veterinario'})

@login_required
@admin_required
def editar_veterinario(request, pk):
    vet = get_object_or_404(Veterinario, pk=pk)
    form_usuario = FormularioUsuario(request.POST or None, instance=vet.usuario)
    form_vet = FormularioVeterinario(request.POST or None, instance=vet)
    if request.method == 'POST':
        if form_usuario.is_valid() and form_vet.is_valid():
            form_usuario.save()
            form_vet.save()
            messages.success(request, 'Veterinario actualizado.')
            return redirect('admin_app:lista_veterinarios')
    return render(request, 'adminApp/veterinarios/formulario.html', {'form_usuario': form_usuario, 'form_vet': form_vet, 'titulo': 'Editar Veterinario'})

@login_required
@admin_required
def lista_citas_admin(request):
    citas = Cita.objects.select_related('id_cliente__usuario', 'id_mascota', 'id_veterinario__usuario', 'id_servicio').all()
    estado = request.GET.get('estado', '')
    fecha = request.GET.get('fecha', '')
    vet_id = request.GET.get('veterinario', '')
    if estado:
        citas = citas.filter(estado_cita=estado)
    if fecha:
        citas = citas.filter(fecha_cita=fecha)
    if vet_id:
        citas = citas.filter(id_veterinario__pk=vet_id)
    citas = citas.order_by('fecha_cita', 'hora_cita')
    veterinarios = Veterinario.objects.select_related('usuario').all()
    return render(request, 'adminApp/citas/lista.html', {'citas': citas, 'veterinarios': veterinarios, 'estado': estado, 'fecha': fecha, 'vet_id': vet_id})

@login_required
@admin_required
def cambiar_estado_cita(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in ['PROGRAMADA', 'COMPLETADA', 'CANCELADA']:
            cita.estado_cita = nuevo_estado
            cita.save()
            messages.success(request, 'Estado de cita actualizado.')
    return redirect('admin_app:lista_citas')

@login_required
@admin_required
def lista_inventario(request):
    UMBRAL = 5
    inventarios = Inventario.objects.select_related('id_tipo_producto').all()
    nombre = request.GET.get('nombre', '')
    categoria = request.GET.get('categoria', '')
    stock = request.GET.get('stock', '')
    if nombre:
        inventarios = inventarios.filter(id_tipo_producto__nombre_producto__icontains=nombre)
    if categoria:
        inventarios = inventarios.filter(id_tipo_producto__categoria__icontains=categoria)
    if stock == 'bajo':
        inventarios = inventarios.filter(cantidad__lte=UMBRAL)
    elif stock == 'disponible':
        inventarios = inventarios.filter(cantidad__gt=UMBRAL)
    entradas_recientes = EntradaProducto.objects.select_related('id_inventario__id_tipo_producto').order_by('-fecha')[:10]
    salidas_recientes = SalidaProducto.objects.select_related('id_inventario__id_tipo_producto').order_by('-fecha')[:10]
    return render(request, 'adminApp/inventario/lista.html', {
        'inventarios': inventarios, 'entradas_recientes': entradas_recientes, 'salidas_recientes': salidas_recientes,
        'UMBRAL': UMBRAL, 'nombre': nombre, 'categoria': categoria, 'stock': stock,
    })

@login_required
@admin_required
def crear_producto(request):
    form = FormularioProducto(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        producto = form.save()
        stock = form.cleaned_data.get('stock_inicial') or 0
        ubicacion = form.cleaned_data.get('ubicacion', '')
        inv = Inventario.objects.create(id_tipo_producto=producto, cantidad=stock, ubicacion=ubicacion)
        if stock > 0:
            EntradaProducto.objects.create(id_inventario=inv, cantidad=stock, observacion='Stock inicial', registrado_por=request.user)
        messages.success(request, 'Producto creado y registrado en inventario.')
        return redirect('admin_app:lista_inventario')
    return render(request, 'adminApp/inventario/formulario_producto.html', {'form': form, 'titulo': 'Crear Producto'})

@login_required
@admin_required
def editar_producto(request, pk):
    producto = get_object_or_404(TipoProducto, pk=pk)
    form = FormularioProducto(request.POST or None, instance=producto)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Producto actualizado.')
        return redirect('admin_app:lista_inventario')
    return render(request, 'adminApp/inventario/formulario_producto.html', {'form': form, 'titulo': 'Editar Producto'})

@login_required
@admin_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(TipoProducto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado.')
        return redirect('admin_app:lista_inventario')
    return render(request, 'adminApp/inventario/confirmar_eliminar.html', {'producto': producto})

@login_required
@admin_required
def registrar_entrada(request):
    form = FormularioEntrada(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        entrada = form.save(commit=False)
        entrada.registrado_por = request.user
        entrada.save()
        inv = entrada.id_inventario
        inv.cantidad += entrada.cantidad
        inv.save()
        messages.success(request, f'Entrada de {entrada.cantidad} unidades registrada.')
        return redirect('admin_app:lista_inventario')
    return render(request, 'adminApp/inventario/formulario_entrada.html', {'form': form, 'titulo': 'Registrar Entrada'})

@login_required
@admin_required
def registrar_salida(request):
    form = FormularioSalida(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        salida = form.save(commit=False)
        salida.registrado_por = request.user
        salida.save()
        inv = salida.id_inventario
        inv.cantidad -= salida.cantidad
        inv.save()
        messages.success(request, f'Salida de {salida.cantidad} unidades registrada.')
        return redirect('admin_app:lista_inventario')
    return render(request, 'adminApp/inventario/formulario_salida.html', {'form': form, 'titulo': 'Registrar Salida'})

@login_required
@admin_required
def lista_servicios(request):
    servicios = TipoServicio.objects.all()
    return render(request, 'adminApp/servicios/lista.html', {'servicios': servicios})

@login_required
@admin_required
def crear_servicio(request):
    form = FormularioServicio(request.POST or None, request.FILES)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Servicio creado exitosamente.')
        return redirect('admin_app:lista_servicios')
    return render(request, 'adminApp/servicios/formulario.html', {'form': form, 'titulo': 'Crear Servicio'})

@login_required
@admin_required
def editar_servicio(request, pk):
    servicio = get_object_or_404(TipoServicio, pk=pk)
    form = FormularioServicio(request.POST or None, request.FILES or None, instance=servicio)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Servicio actualizado.')
        return redirect('admin_app:lista_servicios')
    return render(request, 'adminApp/servicios/formulario.html', {'form': form, 'titulo': 'Editar Servicio', 'servicio': servicio})

@login_required
@admin_required
def eliminar_servicio(request, pk):
    servicio = get_object_or_404(TipoServicio, pk=pk)
    if request.method == 'POST':
        servicio.delete()
        messages.success(request, 'Servicio eliminado.')
        return redirect('admin_app:lista_servicios')
    return render(request, 'adminApp/servicios/confirmar_eliminar.html', {'servicio': servicio})

@login_required
@admin_required
def reportes(request):
    form_ventas = FiltroReporteVentas(request.GET or None)
    form_citas = FiltroReporteCitas(request.GET or None)
    ventas = Venta.objects.filter(estado='COMPLETADO').order_by('-fecha_venta')
    citas = Cita.objects.select_related('id_veterinario__usuario', 'id_servicio').all()

    if form_ventas.is_valid():
        if form_ventas.cleaned_data.get('fecha_desde'):
            ventas = ventas.filter(fecha_venta__date__gte=form_ventas.cleaned_data['fecha_desde'])
        if form_ventas.cleaned_data.get('fecha_hasta'):
            ventas = ventas.filter(fecha_venta__date__lte=form_ventas.cleaned_data['fecha_hasta'])

    if form_citas.is_valid():
        if form_citas.cleaned_data.get('fecha_desde'):
            citas = citas.filter(fecha_cita__gte=form_citas.cleaned_data['fecha_desde'])
        if form_citas.cleaned_data.get('fecha_hasta'):
            citas = citas.filter(fecha_cita__lte=form_citas.cleaned_data['fecha_hasta'])
        if form_citas.cleaned_data.get('estado'):
            citas = citas.filter(estado_cita=form_citas.cleaned_data['estado'])
        if form_citas.cleaned_data.get('id_veterinario'):
            citas = citas.filter(id_veterinario__pk=form_citas.cleaned_data['id_veterinario'])

    total_ventas = ventas.aggregate(t=Sum('total'))['t'] or 0
    total_citas = citas.count()
    citas_por_estado = citas.values('estado_cita').annotate(total=Count('id'))
    citas_por_vet = citas.values('id_veterinario__usuario__nombre','id_veterinario__usuario__apellido').annotate(total=Count('id')).order_by('-total')
    productos_mas_vendidos = DetalleVenta.objects.values('id_inventario__id_tipo_producto__nombre_producto').annotate(total_vendido=Sum('cantidad')).order_by('-total_vendido')[:10]

    return render(request, 'adminApp/reportes/reportes.html', {
        'form_ventas': form_ventas, 'form_citas': form_citas, 'ventas': ventas[:50], 'citas': citas[:50],
        'total_ventas': total_ventas, 'total_citas': total_citas, 'citas_por_estado': citas_por_estado,
        'citas_por_vet': citas_por_vet, 'productos_mas_vendidos': productos_mas_vendidos,
    })

@login_required
@admin_required
def reporte_ventas_pdf(request):
    from adminApp.reportes_pdf import generar_reporte_ventas_pdf
    ventas = Venta.objects.filter(estado='COMPLETADO').order_by('-fecha_venta')
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    if fecha_desde:
        ventas = ventas.filter(fecha_venta__date__gte=fecha_desde)
    if fecha_hasta:
        ventas = ventas.filter(fecha_venta__date__lte=fecha_hasta)
    buffer = generar_reporte_ventas_pdf(ventas)
    return FileResponse(buffer, as_attachment=True, filename='reporte_ventas.pdf')

@login_required
@admin_required
def reporte_clientes_pdf(request):
    from adminApp.reportes_pdf import generar_reporte_clientes_pdf
    clientes = Cliente.objects.select_related('usuario').all()
    buffer = generar_reporte_clientes_pdf(clientes)
    return FileResponse(buffer, as_attachment=True, filename='reporte_clientes.pdf')

@login_required
@admin_required
def reporte_veterinarios_pdf(request):
    from adminApp.reportes_pdf import generar_reporte_veterinarios_pdf
    vets = Veterinario.objects.select_related('usuario').all()
    buffer = generar_reporte_veterinarios_pdf(vets)
    return FileResponse(buffer, as_attachment=True, filename='reporte_veterinarios.pdf')