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
        from django import forms
from django.contrib.auth.models import User
from .models import Reclamo, Categoria

# Formulario para Reclamo
class ReclamoForm(forms.ModelForm):
    class Meta:
        model = Reclamo
        fields = ['descripcion', 'categoria']  # ajusta según tus campos

# Formulario para Usuario (basado en el modelo User de Django)
class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

# Formulario para Categoría
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']   # ajusta según los campos de tu modelo Categoria
class ReclamoForm(forms.ModelForm):
    nombre = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre y Apellido',
            'pattern': '[A-Za-z ]+',
            'title': 'Solo letras y espacios'
        })
    )
    correo = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Correo Electrónico'
        })
    )
    telefono = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Teléfono',
            'pattern': '[0-9]+',
            'title': 'Solo números'
        })
    )
    descripcion = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Descripción del Reclamo'
        })
    )

    class Meta:
        model = Reclamo
        fields = ['nombre','correo','telefono','categoria','descripcion']
class EditarCategoriaReclamoForm(forms.ModelForm):
    class Meta:
        model = Reclamo
        fields = ['categoria']  # ✅ solo este campo

    from django import forms
from django.contrib.auth.models import User

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,  # opcional en edición
        label="Contraseña"
    )
    role = forms.ChoiceField(
        choices=[('admin', 'Administrador'), ('operador', 'Operador')],
        label="Rol"
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
