from django import forms
from django.contrib.auth.models import User
from .models import Reclamo, Categoria

# Formulario para crear un Reclamo
class ReclamoForm(forms.ModelForm):
    nombre = forms.CharField(
        label="Nombre y Apellido",
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre y Apellido',
            'pattern': '[A-Za-z ]+',
            'title': 'Solo letras y espacios'
        })
    )
    correo = forms.EmailField(
        label="Correo Electrónico",
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    telefono = forms.CharField(
        label="Teléfono",
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'pattern': '[0-9]+',
            'title': 'Solo números'
        })
    )
    descripcion = forms.CharField(
        label="Descripción del Reclamo",
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )

    class Meta:
        model = Reclamo
        fields = ['nombre', 'correo', 'telefono', 'categoria', 'descripcion']


# Formulario para consultar reclamos por número
class ConsultaReclamoForm(forms.Form):
    numero_reclamo = forms.IntegerField(
        label="Número de Reclamo",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        error_messages={'invalid': 'Ingrese solo números en el número de reclamo.'}
    )


# Formulario para editar solo la categoría de un reclamo
class EditarCategoriaReclamoForm(forms.ModelForm):
    class Meta:
        model = Reclamo
        fields = ['categoria']


# Formulario para editar reclamos completos
class EditarReclamoForm(forms.ModelForm):
    class Meta:
        model = Reclamo
        fields = ['nombre', 'correo', 'telefono', 'categoria', 'descripcion', 'estado', 'prioridad']


# Formulario para Usuario (basado en el modelo User de Django)
class UsuarioForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Contraseña",
        required=False  # opcional en edición
    )
    role = forms.ChoiceField(
        choices=[('admin', 'Administrador'), ('operador', 'Operador')],
        label="Rol"
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        help_texts = {'username': None}


# Formulario para Categoría
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']

