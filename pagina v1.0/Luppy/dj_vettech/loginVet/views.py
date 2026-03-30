from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Usuario, Rol
from .forms import RegistroForm, LoginForm  # Importamos los nuevos formularios


def logout_view(request):
    logout(request)
    return redirect('inicio')

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            # Extraemos los datos validados del formulario
            user = form.save(commit=False)
            
            # Asignamos el rol por defecto (Asegúrate que 'CLIENTE' existe en tu DB)
            rol_cliente, _ = Rol.objects.get_or_create(nombre='CLIENTE')
            user.rol = rol_cliente
            
            # Guardamos la contraseña de forma segura y el usuario
            user.set_password(form.cleaned_data['password'])
            user.save()
            
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
            
            # Nota: Django usa 'username' internamente aunque sea un correo
            user = authenticate(request, username=correo, password=password)

            if user is not None:
                login(request, user)

                # Redirección según el nombre del Rol
                nombre_rol = user.rol.nombre.upper() # Lo pasamos a mayúsculas para evitar errores
                
                if nombre_rol == 'ADMINISTRADOR':
                    return redirect('admin_dashboard')
                elif nombre_rol == 'VETERINARIO':
                    return redirect('vet_dashboard')
                else:
                    return redirect('inicio')
            else:
                # Opcional: Agregar un mensaje de error si las credenciales fallan
                form.add_error(None, "Correo o contraseña incorrectos")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})