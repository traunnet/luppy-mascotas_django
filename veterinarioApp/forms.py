from django import forms
import json
from clienteApp.models import TipoProducto, Cita, HistorialClinico, Mascota
from loginVet.models import Veterinario, Usuario

class ProductoForm(forms.ModelForm):
    cantidad = forms.IntegerField(
        min_value=0,
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Cantidad en stock'
        })
    )
    ubicacion = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Estante / ubicación'
        })
    )
    class Meta:
        model = TipoProducto
        fields = ['nombre_producto', 'categoria', 'descripcion', 'precio_unitario', 'imagen']
        widgets = {
            'nombre_producto': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
        }

class CitaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Por defecto todas las mascotas (para que el POST no falle)
        self.fields['id_mascota'].queryset = Mascota.objects.all()

        if 'id_cliente' in self.data:
            try:
                cliente_id = int(self.data.get('id_cliente'))
                self.fields['id_mascota'].queryset = Mascota.objects.filter(
                    id_cliente_id=cliente_id
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['id_mascota'].queryset = Mascota.objects.filter(
                id_cliente=self.instance.id_cliente
        )

    class Meta:
        model = Cita
        fields = ['id_cliente', 'id_mascota', 'id_servicio', 'fecha_cita', 'hora_cita', 'motivo', 'estado_cita']
        widgets = {
            'fecha_cita': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_cita': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'motivo': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'id_cliente': forms.Select(attrs={'class': 'form-select', 'id': 'id_cliente'}),
            'id_mascota': forms.Select(attrs={'class': 'form-select', 'id': 'id_mascota'}),
            'id_servicio': forms.Select(attrs={'class': 'form-select'}),
            'estado_cita': forms.Select(attrs={'class': 'form-select'}),
        }

class HistorialForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields['id_cita'].queryset = Cita.objects.filter(
                id_mascota=self.instance.id_mascota
            )
        else:
            self.fields['id_cita'].queryset = Cita.objects.none()

        self.fields['id_cita'].label_from_instance = (
            lambda cita: (
                f"{cita.id_mascota.nombre} | "
                f"{cita.id_servicio} | "
                f"{cita.fecha_cita}"
            )
        )

        if 'id_mascota' in self.data:
            try:
                mascota_id = int(self.data.get('id_mascota'))
                self.fields['id_cita'].queryset = (
                    Cita.objects.filter(id_mascota_id=mascota_id).order_by('-fecha_cita')
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['id_cita'].queryset = (
                Cita.objects.filter(id_mascota=self.instance.id_mascota).order_by('-fecha_cita')
            )

        cita_qs = self.fields['id_cita'].queryset
        mapa_servicios = {str(cita.id): cita.id_servicio_id for cita in cita_qs if cita.id_servicio_id}
        
        self.fields['id_cita'].widget.attrs.update({
            'class': 'form-select',
            'data-servicios': json.dumps(mapa_servicios) 
        })

        self.fields['id_mascota'].widget.attrs.update({
            'class': 'form-select'
        })

        self.fields['id_servicio'].widget.attrs.update({
            'class': 'form-select'
        })

        self.fields['medicacion'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['frecuencia'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['estado'].widget.attrs.update({
            'class': 'form-control'
        })

    class Meta:
        model = HistorialClinico
        fields = [
            'fecha',
            'motivo_consulta',
            'diagnostico',
            'tratamiento',
            'medicacion',
            'frecuencia',
            'estado',
            'id_mascota',
            'id_servicio',
            'id_cita'
        ]
        widgets = {
            'fecha': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
            'motivo_consulta': forms.Textarea(
                attrs={
                    'rows': 3,
                    'class': 'form-control',
                    'placeholder': 'Motivo de la consulta'
                }
            ),
            'diagnostico': forms.Textarea(
                attrs={
                    'rows': 3,
                    'class': 'form-control',
                    'placeholder': 'Diagnóstico médico'
                }
            ),
            'tratamiento': forms.Textarea(
                attrs={
                    'rows': 3,
                    'class': 'form-control',
                    'placeholder': 'Tratamiento indicado'
                }
            ),
            'id_mascota': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),
            'id_servicio': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),
            'id_cita': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),
        }

class ActualizarPerfilForm(forms.ModelForm):
    nombre = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellido = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    correo = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    telefono = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    direccion = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    foto_perfil = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Veterinario
        fields = ['numero_licencia', 'especialidad', 'anios_experiencia']
        widgets = {
            'numero_licencia': forms.TextInput(attrs={'class': 'form-control'}),
            'especialidad': forms.TextInput(attrs={'class': 'form-control'}),
            'anios_experiencia': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ActualizarPerfilForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.usuario:
            self.fields['nombre'].initial = self.instance.usuario.nombre
            self.fields['apellido'].initial = self.instance.usuario.apellido
            self.fields['correo'].initial = self.instance.usuario.correo
            self.fields['telefono'].initial = self.instance.usuario.telefono
            self.fields['direccion'].initial = self.instance.usuario.direccion