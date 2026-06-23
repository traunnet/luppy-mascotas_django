from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Usuario, Rol, Cliente
from .forms import RegistroForm, LoginForm
import datetime


def logout_view(request):
    logout(request)
    return redirect('inicio')


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            rol_cliente, _ = Rol.objects.get_or_create(nombre='CLIENTE')
            user.rol = rol_cliente
            user.set_password(form.cleaned_data['password'])
            user.save()

            Cliente.objects.create(
                usuario=user,
                fecha_registro=datetime.date.today(),
                mascotas_registradas=0
            )

            messages.success(request, 'Cuenta creada exitosamente. Inicia sesión.')
            return redirect('auth_app:login')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():

            correo = form.cleaned_data['correo']
            password = form.cleaned_data['password']

            try:
                usuario = Usuario.objects.get(correo__iexact=correo)

                user = authenticate(
                    request,
                    username=correo,
                    password=password
                )

                if user is not None:

                    login(request, user)

                    nombre_rol = user.rol.nombre.upper()

                    if nombre_rol == 'ADMINISTRADOR':
                        return redirect('admin_app:dashboard')

                    elif nombre_rol == 'VETERINARIO':
                        return redirect('vet_app:dashboard')

                    elif nombre_rol == 'CLIENTE':
                        return redirect('dashboard_cliente')

                    else:
                        return redirect('inicio')

                else:
                    form.add_error(
                        None,
                        'La contraseña es incorrecta.'
                    )

            except Usuario.DoesNotExist:
                form.add_error(
                    None,
                    'No existe una cuenta registrada con ese correo.'
                )

    else:
        form = LoginForm()

    return render(
        request,
        'login.html',
        {'form': form}
    )