from django import forms
from .models import Reclamo


class ReclamoForm(forms.ModelForm):

    class Meta:
        model = Reclamo

        fields = [
            'asunto',
            'descripcion',
            'categoria',
            'prioridad'
        ]

        widgets = {
            'asunto': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'descripcion': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4
                }
            ),

            'categoria': forms.Select(
                attrs={'class': 'form-control'}
            ),

            'prioridad': forms.Select(
                attrs={'class': 'form-control'}
            ),

            class ConsultaReclamoForm(forms.Form):

    numero_reclamo = forms.IntegerField(
        label="Número de Reclamo",
        widget=forms.NumberInput(
            attrs={'class': 'form-control'}
        )
    )
        }