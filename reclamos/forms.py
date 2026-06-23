from django import forms
from django.contrib.auth.models import User
from .models import Reclamo

class ReclamoForm(forms.ModelForm):
    class Meta:
        model = Reclamo
        fields = ['nombre', 'correo', 'telefono', 'categoria', 'descripcion']

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'required': True}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'pattern': '[0-9]+'}),
            'categoria': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'required': True}),
        }

    # Validaciones adicionales
    correo = forms.EmailField(
        label="Correo Electrónico",
        error_messages={'invalid': 'Ingrese un correo válido.'}
    )

    telefono = forms.IntegerField(
        label="Teléfono",
        error_messages={'invalid': 'Ingrese solo números en el teléfono.'}
    )

    nombre = forms.CharField(
        label="Nombre y Apellido",
        error_messages={'required': 'Este campo es obligatorio.'}
    )

    descripcion = forms.CharField(
        label="Descripción del Reclamo",
        widget=forms.Textarea,
        error_messages={'required': 'Debe ingresar una descripción.'}
    )

    # Validación personalizada para nombre
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre.replace(" ", "").isalpha():
            raise forms.ValidationError("El nombre solo puede contener letras y espacios.")
        return nombre


class ConsultaReclamoForm(forms.Form):
    numero_reclamo = forms.IntegerField(
        label="Número de Reclamo",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        error_messages={'invalid': 'Ingrese solo números en el número de reclamo.'}
    )


class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        help_texts = {
        'username': None,  # ✅ esto elimina el texto “Requerido. 150 caracteres…”
    }