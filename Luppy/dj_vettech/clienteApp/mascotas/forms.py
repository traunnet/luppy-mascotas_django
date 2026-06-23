import re
from datetime import date, datetime, timedelta
from django import forms
from django.core.exceptions import ValidationError
from clienteApp.models import Mascota

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

        if edad is not None and fecha_nacimiento:
            años_calculados = (date.today() - fecha_nacimiento).days / 365.25
            if abs(años_calculados - edad) > 2:
                raise ValidationError(
                    'La edad ingresada no es coherente con la fecha de nacimiento. '
                    'Verifica que ambos datos sean correctos.'
                )

        return cleaned_data