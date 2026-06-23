from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum, Count
from datetime import date
from django.http import JsonResponse
# Modelos
from loginVet.models import Veterinario
from clienteApp.models import (
    Cita, HistorialClinico, Inventario, TipoProducto, 
    Venta, DetalleVenta, TipoServicio, Mascota
)
from adminApp.models import EntradaProducto, SalidaProducto

# Formularios
from .forms import CitaForm, ProductoForm, HistorialForm, ActualizarPerfilForm

# ── Dashboard Principal ──────────────────────────────────────────────────────
@login_required
def vet_dashboard(request):
    veterinario = Veterinario.objects.get(usuario=request.user)
    citas_hoy = Cita.objects.filter(
        id_veterinario=veterinario,
        fecha_cita=date.today()
    ).count()
    proximas_citas = Cita.objects.filter(
        id_veterinario=veterinario,
        fecha_cita__gte=date.today(),
        estado_cita='PROGRAMADA'
    ).order_by('fecha_cita')[:5]

    return render(request, 'veterinarioApp/dashboard.html', {
        'veterinario': veterinario,
        'citas_hoy': citas_hoy,
        'proximas_citas': proximas_citas,
    })


# ── Agenda y Gestión de Citas ────────────────────────────────────────────────
def get_mascotas_por_cliente(request, cliente_id):
    mascotas = Mascota.objects.filter(id_cliente_id=cliente_id).values('id', 'nombre')
    return JsonResponse(list(mascotas), safe=False)

def get_citas_por_mascota(request, mascota_id):
    citas = Cita.objects.filter(
        id_mascota_id=mascota_id
    ).values('id', 'fecha_cita', 'id_servicio__tipo')
    
    data = [
        {
            'id': c['id'],
            'label': f"{c['fecha_cita']} | {c['id_servicio__tipo'] or 'Sin servicio'}"
        }
        for c in citas
    ]
    return JsonResponse(data, safe=False)

class AgendaCitasView(LoginRequiredMixin, ListView):
    model = Cita
    template_name = 'veterinarioApp/citas/agenda_citas.html'
    context_object_name = 'citas'

    def get_queryset(self):
        veterinario = Veterinario.objects.get(usuario=self.request.user)
        return Cita.objects.filter(
            id_veterinario=veterinario,
            fecha_cita=date.today()
        ).select_related('id_cliente__usuario', 'id_mascota')


class GestionCitasView(LoginRequiredMixin, ListView):
    model = Cita
    template_name = 'veterinarioApp/citas/gestion_citas.html'
    context_object_name = 'citas'

    def get_queryset(self):
        veterinario = Veterinario.objects.get(usuario=self.request.user)
        return Cita.objects.filter(
            id_veterinario=veterinario
        ).select_related('id_cliente__usuario', 'id_mascota').order_by('fecha_cita', 'hora_cita')


class CrearCitaView(LoginRequiredMixin, CreateView):
    model = Cita
    form_class = CitaForm
    template_name = 'veterinarioApp/citas/crear_cita.html'
    success_url = reverse_lazy('vet_app:gestion_citas')

    def form_valid(self, form):
        form.instance.id_veterinario = Veterinario.objects.get(usuario=self.request.user)
        return super().form_valid(form)


class ActualizarCitaView(LoginRequiredMixin, UpdateView):
    model = Cita
    form_class = CitaForm
    template_name = 'veterinarioApp/citas/actualizar_cita.html'
    success_url = reverse_lazy('vet_app:gestion_citas')

    def form_invalid(self, form):
        print("ERRORES DEL FORM:", form.errors)  # <-- agrega esto
        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        estado = self.request.GET.get('estado')
        if estado:
            initial['estado_cita'] = estado.upper()
        return initial


class EliminarCitaView(LoginRequiredMixin, DeleteView):
    model = Cita
    template_name = 'veterinarioApp/citas/eliminar_cita.html'
    success_url = reverse_lazy('vet_app:gestion_citas')


# ── Historial Clínico ────────────────────────────────────────────────────────
class HistorialClinicoView(LoginRequiredMixin, ListView):
    model = HistorialClinico
    template_name = 'veterinarioApp/historial/historial_clinico.html'
    context_object_name = 'historiales'

    def get_queryset(self):
        veterinario = Veterinario.objects.get(usuario=self.request.user)
        queryset = HistorialClinico.objects.filter(
            id_veterinario=veterinario
        ).select_related('id_mascota')
        
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(id_mascota__nombre__icontains=query) |
                Q(tratamiento__icontains=query) |
                Q(diagnostico__icontains=query)
            )
        return queryset


class CrearHistorialView(LoginRequiredMixin, CreateView):
    model = HistorialClinico
    form_class = HistorialForm 
    template_name = 'veterinarioApp/historial/crear_historial.html'
    success_url = reverse_lazy('vet_app:historial_clinico')

    def form_valid(self, form):
        form.instance.id_veterinario = Veterinario.objects.get(usuario=self.request.user)
        return super().form_valid(form)


class ActualizarHistorialView(LoginRequiredMixin, UpdateView):
    model = HistorialClinico
    form_class = HistorialForm
    template_name = 'veterinarioApp/historial/actualizar_historial.html'
    success_url = reverse_lazy('vet_app:historial_clinico')

    def form_invalid(self, form):
        print("ERRORES HISTORIAL:", form.errors)
        return super().form_invalid(form)


# ── Inventario y Productos ───────────────────────────────────────────────────
class InventarioListView(LoginRequiredMixin, ListView):
    model = Inventario
    template_name = 'veterinarioApp/ventas/inventario.html'
    context_object_name = 'inventarios'

    def get_queryset(self):
        queryset = Inventario.objects.select_related('id_tipo_producto')
        nombre = self.request.GET.get('nombre')
        categoria = self.request.GET.get('categoria')
        stock = self.request.GET.get('stock')

        if nombre:
            queryset = queryset.filter(id_tipo_producto__nombre_producto__icontains=nombre)
        if categoria:
            queryset = queryset.filter(id_tipo_producto__categoria__icontains=categoria)
        if stock:
            if stock == 'bajo': queryset = queryset.filter(cantidad__lt=5)
            elif stock == 'alto': queryset = queryset.filter(cantidad__gte=5)
        return queryset

class CrearProductoView(LoginRequiredMixin, CreateView):
    model = TipoProducto
    form_class = ProductoForm
    template_name = 'veterinarioApp/producto/crear_producto.html'
    success_url = reverse_lazy('vet_app:lista_inventario')
    def form_valid(self, form):
        response = super().form_valid(form)
        Inventario.objects.create(
            id_tipo_producto=self.object,
            cantidad=form.cleaned_data['cantidad'],
            ubicacion=form.cleaned_data['ubicacion']
        )
        return response

class ActualizarProductoView(LoginRequiredMixin, UpdateView):
    model = TipoProducto
    form_class = ProductoForm
    template_name = 'veterinarioApp/producto/actualizar_producto.html'
    success_url = reverse_lazy('vet_app:lista_inventario')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        inventario, _ = Inventario.objects.get_or_create(
            id_tipo_producto=self.object
        )
        inventario.cantidad = form.cleaned_data['cantidad']
        inventario.ubicacion = form.cleaned_data['ubicacion']
        inventario.save()
        return response
    
class EliminarProductoView(LoginRequiredMixin, DeleteView):
    model = TipoProducto
    template_name = 'veterinarioApp/producto/eliminar_producto.html'
    success_url = reverse_lazy('vet_app:lista_inventario')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        producto = self.object
        context['inventario'] = Inventario.objects.filter(id_tipo_producto=producto).first()
        return context


# ── Entradas y Salidas de Stock ──────────────────────────────────────────────
class CrearEntradaProductoView(LoginRequiredMixin, CreateView):
    model = EntradaProducto
    template_name = 'veterinarioApp/producto/crear_entrada.html'
    fields = ['id_inventario', 'cantidad', 'precio_compra', 'proveedor', 'observacion']
    success_url = reverse_lazy('vet_app:lista_inventario')

    def form_valid(self, form):
        entrada = form.save(commit=False)
        entrada.registrado_por = self.request.user
        entrada.save()

        inventario = entrada.id_inventario
        inventario.cantidad += entrada.cantidad
        inventario.save()
        return redirect(self.success_url)


class CrearSalidaProductoView(LoginRequiredMixin, CreateView):
    model = SalidaProducto
    template_name = 'veterinarioApp/producto/crear_salida.html'
    fields = ['id_inventario', 'cantidad', 'motivo', 'observacion']
    success_url = reverse_lazy('vet_app:lista_inventario')

    def form_valid(self, form):
        salida = form.save(commit=False)
        inventario = salida.id_inventario

        if inventario.cantidad < salida.cantidad:
            form.add_error('cantidad', 'Stock insuficiente')
            return self.form_invalid(form)

        salida.registrado_por = self.request.user
        salida.save()

        inventario.cantidad -= salida.cantidad
        inventario.save()
        return redirect(self.success_url)


# ── Ventas ───────────────────────────────────────────────────────────────────
class VentaListView(LoginRequiredMixin, ListView):
    model = Venta
    template_name = 'veterinarioApp/ventas/ventas.html'
    context_object_name = 'ventas'

    def get_queryset(self):
        queryset = Venta.objects.all()
        fecha = self.request.GET.get('fecha')
        estado = self.request.GET.get('estado')
        total = self.request.GET.get('total')

        if fecha: queryset = queryset.filter(fecha_venta=fecha)
        if estado: queryset = queryset.filter(estado__icontains=estado)
        if total: queryset = queryset.filter(total__gte=total)
        return queryset


class CrearVentaView(LoginRequiredMixin, View):
    template_name = 'veterinarioApp/ventas/crear_venta.html'
    success_url = reverse_lazy('vet_app:ventas')

    def get(self, request):
        inventarios = Inventario.objects.select_related('id_tipo_producto')
        return render(request, self.template_name, {'inventarios': inventarios})

    def post(self, request):
        inventario_id = request.POST.get('producto')
        cantidad = int(request.POST.get('cantidad'))
        inventario = Inventario.objects.get(id=inventario_id)

        if inventario.cantidad < cantidad:
            return render(request, self.template_name, {
                'inventarios': Inventario.objects.all(),
                'error': 'Stock insuficiente'
            })
        veterinario = Veterinario.objects.get(usuario=request.user)    
        venta = Venta.objects.create(id_vet=veterinario, estado='COMPLETADO')
        precio = inventario.id_tipo_producto.precio_unitario

        DetalleVenta.objects.create(
            id_venta=venta,
            id_inventario=inventario,
            cantidad=cantidad,
            precio_unitario=precio
        )

        total = precio * cantidad
        venta.total = total
        venta.save()

        inventario.cantidad -= cantidad
        inventario.save()
        return redirect(self.success_url)


# ── Reportes y Perfil ────────────────────────────────────────────────────────
class ReporteGeneralView(ListView):
    model = Venta
    template_name = 'veterinarioApp/reportes.html'
    context_object_name = 'ventas'

    def get_queryset(self):
        queryset = Venta.objects.all()
        fecha_inicio = self.request.GET.get('fecha_inicio')
        fecha_fin = self.request.GET.get('fecha_fin')
        estado = self.request.GET.get('estado')

        if fecha_inicio: queryset = queryset.filter(fecha_venta__gte=fecha_inicio)
        if fecha_fin: queryset = queryset.filter(fecha_venta__lte=fecha_fin)
        if estado: queryset = queryset.filter(estado=estado)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ventas = self.get_queryset()
        context['total_ventas'] = ventas.aggregate(Sum('total'))['total__sum'] or 0
        context['cantidad_ventas'] = ventas.count()
        context['productos_vendidos'] = DetalleVenta.objects.aggregate(Sum('cantidad'))['cantidad__sum'] or 0
        return context


class PerfilView(LoginRequiredMixin, DetailView):
    model = Veterinario
    template_name = 'veterinarioApp/perfil/perfil.html'
    context_object_name = 'perfil'

    def get_object(self):
        veterinario, _ = Veterinario.objects.get_or_create(
            usuario=self.request.user,
            defaults={'numero_licencia': f'LIC-{self.request.user.pk}'}
        )
        return veterinario

class ActualizarPerfilView(LoginRequiredMixin, View):
    template_name = 'veterinarioApp/perfil/actualizar_perfil.html'

    def get(self, request):
        perfil = Veterinario.objects.get(usuario=request.user)
        form = ActualizarPerfilForm(instance=perfil) 
        return render(request, self.template_name, {'form': form, 'perfil': perfil})

    def post(self, request):
        perfil = Veterinario.objects.get(usuario=request.user)
        form = ActualizarPerfilForm(request.POST, request.FILES, instance=perfil)
        
        if form.is_valid():
            perfil_guardado = form.save()
            user = perfil_guardado.usuario
            user.nombre = form.cleaned_data['nombre']
            user.apellido = form.cleaned_data['apellido']
            user.correo = form.cleaned_data['correo']
            user.telefono = form.cleaned_data['telefono']
            user.direccion = form.cleaned_data['direccion']
            if 'foto_perfil' in request.FILES:
                user.foto_perfil = request.FILES['foto_perfil']
            user.save()
            return redirect('vet_app:perfil')
            
        return render(request, self.template_name, {'form': form, 'perfil': perfil})