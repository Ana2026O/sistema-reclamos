from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from .models import Reclamo, Estado
from .forms import ReclamoForm, ConsultaReclamoForm


def inicio(request):
    return render(request, 'reclamos/inicio.html')


def registrar_reclamo(request):

    if request.method == 'POST':
        form = ReclamoForm(request.POST)

        if form.is_valid():

            reclamo = form.save(commit=False)

            reclamo.usuario = User.objects.first()

            reclamo.estado = Estado.objects.get(nombre='Nuevo')

            reclamo.save()

            return redirect(
                'confirmacion_reclamo',
                reclamo_id=reclamo.id
            )

    else:
        form = ReclamoForm()

    return render(
        request,
        'reclamos/registrar_reclamo.html',
        {'form': form}
    )
