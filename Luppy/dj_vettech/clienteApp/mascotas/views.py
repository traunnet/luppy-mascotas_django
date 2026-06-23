from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from clienteApp.models import Mascota, HistorialClinico
from clienteApp.mascotas.forms import FormularioMascota, RAZAS_POR_ESPECIE


def get_cliente(user):
    from loginVet.models import Cliente
    cliente, _ = Cliente.objects.get_or_create(usuario=user)
    return cliente


@login_required
def lista_mascotas(request):
    mascotas = Mascota.objects.filter(id_cliente=get_cliente(request.user))
    return render(request, 'clienteApp/mascotas/lista.html', {'mascotas': mascotas})


@login_required
def crear_mascota(request):
    if request.method == 'POST':
        form = FormularioMascota(request.POST)
        if form.is_valid():
            mascota = form.save(commit=False)
            mascota.id_cliente = get_cliente(request.user)
            mascota.save()
            messages.success(request, f'¡{mascota.nombre} ha sido registrado exitosamente!')
            return redirect('lista_mascotas')
    else:
        form = FormularioMascota()
    return render(request, 'clienteApp/mascotas/formulario.html', {'form': form})


@login_required
def editar_mascota(request, pk):
    mascota = get_object_or_404(Mascota, pk=pk, id_cliente=get_cliente(request.user))
    if request.method == 'POST':
        form = FormularioMascota(request.POST, instance=mascota)
        if form.is_valid():
            form.save()
            messages.success(request, f'¡Los datos de {mascota.nombre} han sido actualizados!')
            return redirect('lista_mascotas')
    else:
        form = FormularioMascota(instance=mascota)
    return render(request, 'clienteApp/mascotas/formulario.html', {'form': form})


@login_required
def eliminar_mascota(request, pk):
    mascota = get_object_or_404(Mascota, pk=pk, id_cliente=get_cliente(request.user))
    if request.method == 'POST':
        nombre = mascota.nombre
        mascota.delete()
        messages.success(request, f'{nombre} ha sido eliminado correctamente.')
        return redirect('lista_mascotas')
    return render(request, 'clienteApp/mascotas/confirmar_eliminar.html', {'mascota': mascota})


@login_required
def historial_clinico(request, id_mascota):
    mascota = get_object_or_404(Mascota, pk=id_mascota, id_cliente=get_cliente(request.user))
    historial = HistorialClinico.objects.filter(id_mascota=mascota)
    return render(request, 'clienteApp/mascotas/historial_clinico.html', {
        'mascota': mascota,
        'historial': historial
    })


def obtener_razas(request):
    especie = request.GET.get('especie')
    razas = RAZAS_POR_ESPECIE.get(especie, [])
    return JsonResponse({'razas': razas})