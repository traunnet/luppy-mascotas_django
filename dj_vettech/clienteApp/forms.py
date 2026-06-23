from datetime import datetime, timedelta
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Mascota, Cita, Cliente
from loginVet.models import Veterinario
from loginVet.validators import NAME_REGEX, name_validator, PHONE_REGEX, phone_validator


import re
from datetime import date
from datetime import datetime, timedelta
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Mascota, Cita, Cliente
from loginVet.models import Veterinario
from loginVet.validators import NAME_REGEX, name_validator, PHONE_REGEX, phone_validator

RAZAS_POR_ESPECIE = {
    'Perro': ['Labrador', 'Pug', 'Pastor Alemán', 'Bulldog'],
    'Gato': ['Persa', 'Siamés', 'Bengala'],
}

EDAD_MAXIMA_POR_ESPECIE = {
    'Perro': 20,
    'Gato': 25,
}

class FormularioMascota(forms.ModelForm):

    especie = forms.ChoiceField(
        choices=[('', 'Seleccione una especie')] + [(k, k) for k in RAZAS_POR_ESPECIE.keys()],
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_especie'})
    )

    raza = forms.ChoiceField(
        choices=[('', 'Primero seleccione una especie')],
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_raza'})
    )

    class Meta:
        model = Mascota
        fields = ['nombre', 'especie', 'raza', 'sexo', 'color', 'edad', 'fecha_nacimiento']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        especie = self.data.get('especie') or (self.instance.especie if self.instance.pk else None)
        if especie:
            self.fields['raza'].choices = [('', 'Seleccione una raza')] + [
                (r, r) for r in RAZAS_POR_ESPECIE.get(especie, [])
            ]

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if not nombre:
            raise ValidationError('El nombre de la mascota es obligatorio.')
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s\-]+$', nombre):
            raise ValidationError('El nombre solo puede contener letras y espacios, sin números ni caracteres especiales.')
        if len(nombre) < 2:
            raise ValidationError('El nombre debe tener al menos 2 caracteres.')
        if len(nombre) > 50:
            raise ValidationError('El nombre no puede superar los 50 caracteres.')
        return nombre.capitalize()

    def clean_color(self):
        color = self.cleaned_data.get('color', '').strip()
        if color and not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s\/\-]+$', color):
            raise ValidationError('El color solo puede contener letras (ej: café, blanco y negro).')
        return color

    def clean_edad(self):
        edad = self.cleaned_data.get('edad')
        especie = self.data.get('especie')
        if edad is not None:
            if edad < 0:
                raise ValidationError('La edad no puede ser negativa.')
            max_edad = EDAD_MAXIMA_POR_ESPECIE.get(especie, 30)
            if edad > max_edad:
                raise ValidationError(
                    f'La edad máxima para un {especie or "animal"} es de {max_edad} años. '
                    f'Si tu mascota tiene más edad, verifica el dato.'
                )
        return edad

    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data.get('fecha_nacimiento')
        if fecha:
            hoy = date.today()
            if fecha > hoy:
                raise ValidationError('La fecha de nacimiento no puede ser una fecha futura.')
            años = (hoy - fecha).days / 365.25
            especie = self.data.get('especie')
            max_edad = EDAD_MAXIMA_POR_ESPECIE.get(especie, 30)
            if años > max_edad:
                raise ValidationError(
                    f'La fecha de nacimiento indica más de {max_edad} años, '
                    f'lo cual no es posible para un {especie or "animal"} de esta especie.'
                )
            if fecha.year < 1990:
                raise ValidationError('La fecha de nacimiento parece incorrecta. Verifica el año ingresado.')
        return fecha

    def clean(self):
        cleaned_data = super().clean()
        especie = cleaned_data.get('especie')
        raza = cleaned_data.get('raza')
        edad = cleaned_data.get('edad')
        fecha_nacimiento = cleaned_data.get('fecha_nacimiento')

        if especie and raza:
            if raza not in RAZAS_POR_ESPECIE.get(especie, []):
                raise ValidationError('La raza no corresponde a la especie seleccionada.')

        # Coherencia entre edad y fecha de nacimiento
        if edad is not None and fecha_nacimiento:
            años_calculados = (date.today() - fecha_nacimiento).days / 365.25
            if abs(años_calculados - edad) > 2:
                raise ValidationError(
                    'La edad ingresada no es coherente con la fecha de nacimiento. '
                    'Verifica que ambos datos sean correctos.'
                )

        return cleaned_data


class FormularioCita(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['id_mascota', 'id_veterinario', 'id_servicio', 'fecha_cita', 'hora_cita', 'motivo']
        widgets = {
            'id_mascota': forms.Select(attrs={'class': 'form-control'}),
            'id_veterinario': forms.Select(attrs={'class': 'form-control'}),
            'id_servicio': forms.Select(attrs={'class': 'form-control'}),
            'fecha_cita': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora_cita': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Motivo de la cita'}),
        }
        labels = {
            'id_mascota': 'Mascota',
            'id_veterinario': 'Veterinario',
            'id_servicio': 'Servicio',
            'fecha_cita': 'Fecha',
            'hora_cita': 'Hora',
            'motivo': 'Motivo',
        }

    def __init__(self, *args, usuario=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario = usuario

        if usuario and hasattr(usuario, 'cliente'):
            self.fields['id_mascota'].queryset = Mascota.objects.filter(id_cliente=usuario.cliente)

        self.fields['id_veterinario'].queryset = Veterinario.objects.select_related('usuario').all()
        self.fields['id_veterinario'].empty_label = 'Selecciona un veterinario'
        self.fields['id_servicio'].empty_label = 'Selecciona un servicio'

    def clean(self):
        cleaned_data = super().clean()

        mascota = cleaned_data.get('id_mascota')
        veterinario = cleaned_data.get('id_veterinario')
        servicio = cleaned_data.get('id_servicio')
        fecha = cleaned_data.get('fecha_cita')
        hora = cleaned_data.get('hora_cita')

        if not all([mascota, veterinario, servicio, fecha, hora]):
            return cleaned_data

        tz = timezone.get_current_timezone()
        inicio_cita = timezone.make_aware(datetime.combine(fecha, hora), tz)

        if inicio_cita <= timezone.now():
            raise ValidationError('La cita no se puede crear, revisa nuevos horarios.')

        duracion_servicio = int(getattr(servicio, 'duracion_minutos', 30) or 30)
        fin_cita = inicio_cita + timedelta(minutes=duracion_servicio)

        cita_actual = self.instance.pk

        # 1) La mascota no puede tener otra cita el mismo día
        citas_mascota = Cita.objects.filter(
            id_mascota=mascota,
            fecha_cita=fecha
        ).exclude(estado_cita__iexact='CANCELADA')

        if cita_actual:
            citas_mascota = citas_mascota.exclude(pk=cita_actual)

        if citas_mascota.exists():
            raise ValidationError(
                'La mascota ya posee una cita este mismo día, debes esperar a que termine primero.'
            )

        # 2) El veterinario no puede estar ocupado en esa franja horaria
        citas_veterinario = Cita.objects.filter(
            id_veterinario=veterinario,
            fecha_cita=fecha
        ).exclude(estado_cita__iexact='CANCELADA')

        if cita_actual:
            citas_veterinario = citas_veterinario.exclude(pk=cita_actual)

        for cita_existente in citas_veterinario.select_related('id_servicio'):
            inicio_existente = timezone.make_aware(
                datetime.combine(cita_existente.fecha_cita, cita_existente.hora_cita),
                tz
            )
            duracion_existente = int(getattr(cita_existente.id_servicio, 'duracion_minutos', 30) or 30)
            fin_existente = inicio_existente + timedelta(minutes=duracion_existente)

            hay_cruce = inicio_cita < fin_existente and fin_cita > inicio_existente
            if hay_cruce:
                raise ValidationError(
                    'Este doctor se encuentra en cita a este horario, por favor prueba con otra hora o fecha.'
                )

        return cleaned_data


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'pattern': NAME_REGEX}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'pattern': NAME_REGEX}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '300 123 4567', 'pattern': PHONE_REGEX}),
            'tipo_doc': forms.Select(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }