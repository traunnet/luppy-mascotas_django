from django import forms
import re
from .models import Usuario
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
from .validators import (
    NAME_REGEX, PHONE_REGEX,
    name_validator, phone_validator,
    cedula_validator, validate_nit
)
Usuario = get_user_model()

class RegistroForm(forms.ModelForm):

    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'autocomplete': 'new-password'
        })
    )

    nombre = forms.CharField(
        max_length=50,
        validators=[name_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombres',
            'pattern': NAME_REGEX,
            'autocomplete': 'given-name'
        })
    )

    apellido = forms.CharField(
        max_length=50,
        validators=[name_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apellidos',
            'pattern': NAME_REGEX,
            'autocomplete': 'family-name'
        })
    )

    correo = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com',
            'autocomplete': 'email'
        })
    )

    telefono = forms.CharField(
        required=False,
        validators=[phone_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '3001234567',
            'type': 'tel',
            'inputmode': 'numeric',
            'maxlength': '10',
            'minlength': '10',
            'pattern': r'^3\d{9}$',
            'autocomplete': 'tel'
        })
    )

    tipo_doc = forms.ChoiceField(
        choices=Usuario.TIPO_DOC_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    numero_documento = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Número de documento',
            'inputmode': 'numeric',
            'autocomplete': 'off'
        })
    )

    direccion = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Dirección',
            'autocomplete': 'street-address'
        })
    )

    class Meta:
        model = Usuario
        fields = [
            'tipo_doc',
            'numero_documento',
            'nombre',
            'apellido',
            'correo',
            'telefono',
            'direccion',
            'password'
        ]

    def clean_correo(self):
        correo = (self.cleaned_data.get('correo') or '').strip().lower()

        if Usuario.objects.filter(correo__iexact=correo).exists():
            raise forms.ValidationError(
                'Ya existe una cuenta registrada con este correo.'
            )

        return correo

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')

        if not telefono:
            return None

        t = re.sub(r'\s+', '', str(telefono).strip())

        if not t.isdigit():
            raise forms.ValidationError(
                'El teléfono solo debe contener números.'
            )

        if not re.match(r'^3\d{9}$', t):
            raise forms.ValidationError(
                'El teléfono celular debe tener exactamente 10 dígitos y empezar por 3.'
            )

        if Usuario.objects.filter(telefono=t).exists():
            raise forms.ValidationError(
                'Ya existe una cuenta registrada con este teléfono.'
            )

        return t

    def clean_numero_documento(self):
        numero = (self.cleaned_data.get('numero_documento') or '').strip()
        tipo = self.cleaned_data.get('tipo_doc')

        if not numero:
            raise forms.ValidationError(
                'El número de documento es obligatorio.'
            )

        valor = re.sub(r'[^0-9\-]', '', numero)

        if tipo in ['CC', 'TI', 'CE']:
            if not re.match(r'^\d{6,10}$', valor):
                raise forms.ValidationError(
                    'Documento inválido. Ingrese entre 6 y 10 dígitos, sin puntos ni espacios.'
                )

        elif tipo == 'NIT':
            validate_nit(valor)

        else:
            raise forms.ValidationError(
                'Tipo de documento no válido.'
            )

        if Usuario.objects.filter(numero_documento__iexact=valor).exists():
            raise forms.ValidationError(
                'Ya existe una cuenta registrada con este número de documento.'
            )

        return valor

    def clean_nombre(self):
        nombre = (self.cleaned_data.get('nombre') or '').strip()
        return nombre

    def clean_apellido(self):
        apellido = (self.cleaned_data.get('apellido') or '').strip()
        return apellido

    def clean_direccion(self):
        direccion = (self.cleaned_data.get('direccion') or '').strip()
        return direccion
    

class LoginForm(forms.Form):
    correo = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class PerfilForm(forms.ModelForm):
    """Form para actualizar perfil de `Usuario` con validaciones cliente/servidor."""
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'telefono', 'tipo_doc', 'numero_documento', 'direccion', 'foto_perfil']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres', 'pattern': NAME_REGEX}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos', 'pattern': NAME_REGEX}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '300 123 4567', 'pattern': PHONE_REGEX}),
            'tipo_doc': forms.Select(attrs={'class': 'form-control'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de documento'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección completa'}),
            'foto_perfil': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono:
            t = telefono.strip()
            t_clean = re.sub(r'\s+', '', t)
            if not t_clean.isdigit():
                raise forms.ValidationError('Teléfono solo debe contener dígitos y espacios.')
            if not re.match(r'^3\d{9}$', t_clean):
                raise forms.ValidationError('Teléfono inválido. Use formato: 300 123 4567')
            # Normalize to spaced format: 300 123 4567
            return f"{t_clean[:3]} {t_clean[3:6]} {t_clean[6:]}"
        return telefono

    def clean_numero_documento(self):
        numero = self.cleaned_data.get('numero_documento')
        tipo = self.cleaned_data.get('tipo_doc')
        if not numero:
            return numero
        v = re.sub(r'[^0-9\-]', '', str(numero))
        # Validaciones por tipo
        if tipo == 'CC':
            if not re.match(r'^\d{6,10}$', v):
                raise forms.ValidationError('Cédula inválida. Ingrese sin puntos ni espacios (6-10 dígitos).')
            return v
        if tipo == 'NIT':
            try:
                validate_nit(v)
            except Exception as e:
                raise forms.ValidationError(str(e))
            return v
        # Fallback: aceptar solo dígitos
        if not re.match(r'^\d+$', v):
            raise forms.ValidationError('Número de documento inválido.')
        return v
    
class CustomPasswordResetForm(PasswordResetForm):

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ejemplo@correo.com',
            'required': True,
            'autocomplete': 'email'
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not Usuario.objects.filter(
            correo__iexact=email,
            is_active=True
        ).exists():

            raise forms.ValidationError(
                'No existe una cuenta registrada con este correo. Debes registrarte primero.'
            )

        return email

    def get_users(self, email):
        return Usuario.objects.filter(
            correo__iexact=email,
            is_active=True
        )