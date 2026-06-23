from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import FormularioCita
from .models import Cita
from loginVet.models import Cliente


def get_cliente(user):
    cliente, _ = Cliente.objects.get_or_create(usuario=user)
    return cliente


@login_required
def lista_citas(request):
    cliente = get_cliente(request.user)
    citas = (
        Cita.objects.filter(id_cliente=cliente)
        .select_related('id_mascota', 'id_veterinario__usuario', 'id_servicio')
        .order_by('fecha_cita', 'hora_cita')
    )
    return render(request, 'clienteApp/lista_citas.html', {'citas': citas})


@login_required
def crear_cita(request):
    cliente = get_cliente(request.user)

    if request.method == 'POST':
        form = FormularioCita(request.POST, usuario=request.user)

        if form.is_valid():
            with transaction.atomic():
                cita = form.save(commit=False)
                cita.id_cliente = cliente
                cita.estado_cita = 'PROGRAMADA'
                cita.save()

            messages.success(request, 'Cita agendada exitosamente.')
            return redirect('lista_citas')

    else:
        form = FormularioCita(usuario=request.user)

    return render(request, 'clienteApp/formulario_cita.html', {'form': form})


@login_required
def eliminar_cita(request, pk):
    cliente = get_cliente(request.user)
    cita = get_object_or_404(Cita, pk=pk, id_cliente=cliente)

    if request.method == 'POST':
        # Eliminación lógica: se conserva el historial
        if cita.estado_cita.upper() != 'CANCELADA':
            cita.estado_cita = 'CANCELADA'
            cita.save(update_fields=['estado_cita'])
            messages.success(request, 'Cita eliminada correctamente.')
        else:
            messages.info(request, 'Esta cita ya estaba cancelada.')

    return redirect('lista_citas')