from django import forms
import re
from decimal import Decimal, InvalidOperation
from loginVet.models import Usuario, Rol, Veterinario, Cliente
from clienteApp.models import TipoProducto, Inventario, TipoServicio, Cita
from .models import EntradaProducto, SalidaProducto
from loginVet.validators import (
    NAME_REGEX, PHONE_REGEX, CURRENCY_REGEX,
    name_validator, phone_validator, validate_nit
)


class FormularioUsuario(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        label='Contraseña',
        help_text='Dejar vacío para no cambiar.'
    )

    class Meta:
        model = Usuario
        fields = [
            'nombre', 'apellido', 'correo', 'telefono',
            'direccion', 'tipo_doc', 'numero_documento',
            'rol', 'is_active'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres', 'pattern': NAME_REGEX}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos', 'pattern': NAME_REGEX}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '300 123 4567', 'pattern': PHONE_REGEX}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección completa'}),
            'tipo_doc': forms.Select(attrs={'class': 'form-select'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de documento'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        pw = self.cleaned_data.get('password')
        if pw:
            user.set_password(pw)
        if commit:
            user.save()
        return user

    def clean_numero_documento(self):
        numero = self.cleaned_data.get('numero_documento')
        tipo = self.cleaned_data.get('tipo_doc')

        if not numero:
            return numero

        v = re.sub(r'[^0-9\-]', '', str(numero))

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

        if not re.match(r'^\d+$', v):
            raise forms.ValidationError('Número de documento inválido.')

        return v


class FormularioVeterinario(forms.ModelForm):

    class Meta:
        model = Veterinario
        fields = ['numero_licencia', 'especialidad', 'anios_experiencia']
        widgets = {
            'numero_licencia': forms.TextInput(attrs={'class': 'form-control'}),
            'especialidad': forms.TextInput(attrs={'class': 'form-control'}),
            'anios_experiencia': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class FormularioProducto(forms.ModelForm):

    stock_inicial = forms.IntegerField(
        min_value=0,
        initial=0,
        required=False,
        label='Stock inicial',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    ubicacion = forms.CharField(
        max_length=100,
        required=False,
        label='Ubicación en bodega',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = TipoProducto
        fields = ['nombre_producto', 'categoria', 'descripcion', 'precio_unitario']
        widgets = {
            'nombre_producto': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'precio_unitario': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00',
                'inputmode': 'decimal',
                'pattern': CURRENCY_REGEX
            }),
        }

    def clean_precio_unitario(self):
        precio = self.cleaned_data.get('precio_unitario')

        if precio is None:
            return precio

        try:
            if Decimal(precio) < Decimal('0'):
                raise forms.ValidationError('El precio debe ser mayor o igual a 0.')
        except (InvalidOperation, TypeError):
            raise forms.ValidationError('Precio inválido.')

        return precio


class FormularioEntrada(forms.ModelForm):

    class Meta:
        model = EntradaProducto
        fields = ['id_inventario', 'cantidad', 'precio_compra', 'proveedor', 'observacion']
        widgets = {
            'id_inventario': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'precio_compra': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00',
                'inputmode': 'decimal',
                'pattern': CURRENCY_REGEX
            }),
            'proveedor': forms.TextInput(attrs={'class': 'form-control'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
        labels = {
            'id_inventario': 'Producto en inventario',
            'precio_compra': 'Precio de compra (opcional)',
        }


class FormularioSalida(forms.ModelForm):

    class Meta:
        model = SalidaProducto
        fields = ['id_inventario', 'cantidad', 'motivo', 'observacion']
        widgets = {
            'id_inventario': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'motivo': forms.Select(attrs={'class': 'form-select'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
        labels = {
            'id_inventario': 'Producto en inventario',
        }

    def clean(self):
        cleaned = super().clean()
        inventario = cleaned.get('id_inventario')
        cantidad = cleaned.get('cantidad')

        if inventario and cantidad:
            if cantidad > inventario.cantidad:
                raise forms.ValidationError(
                    f'Stock insuficiente. Solo hay {inventario.cantidad} unidades.'
                )

        return cleaned


class FormularioServicio(forms.ModelForm):

    class Meta:
        model = TipoServicio
        fields = ['tipo', 'descripcion', 'precio', 'duracion']
        widgets = {
            'tipo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00',
                'inputmode': 'decimal',
                'pattern': CURRENCY_REGEX
            }),
            'duracion': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')

        if precio is None:
            return precio

        try:
            if Decimal(precio) < Decimal('0'):
                raise forms.ValidationError('El precio debe ser mayor o igual a 0.')
        except (InvalidOperation, TypeError):
            raise forms.ValidationError('Precio inválido.')

        return precio


class FiltroReporteVentas(forms.Form):

    fecha_desde = forms.DateField(
        required=False,
        label='Desde',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    fecha_hasta = forms.DateField(
        required=False,
        label='Hasta',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    estado = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Todos'),
            ('COMPLETADO', 'Completado'),
            ('CARRITO', 'Carrito')
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class FiltroReporteCitas(forms.Form):

    fecha_desde = forms.DateField(
        required=False,
        label='Desde',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    fecha_hasta = forms.DateField(
        required=False,
        label='Hasta',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    estado = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Todos'),
            ('PROGRAMADA', 'Programada'),
            ('COMPLETADA', 'Completada'),
            ('CANCELADA', 'Cancelada')
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    id_veterinario = forms.ChoiceField(
        required=False,
        label='Veterinario',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        from loginVet.models import Veterinario

        vets = Veterinario.objects.select_related('usuario').all()

        self.fields['id_veterinario'].choices = (
            [('', 'Todos')] +
            [(v.pk, str(v.usuario)) for v in vets]
        )