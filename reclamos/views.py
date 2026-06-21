from django.shortcuts import render
from .forms import ReclamoForm


def inicio(request):
    return render(request, 'reclamos/inicio.html')


def registrar_reclamo(request):

    form = ReclamoForm()

    return render(
        request,
        'reclamos/registrar_reclamo.html',
        {'form': form}
    )