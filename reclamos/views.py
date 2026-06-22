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


def confirmacion_reclamo(request):
    return render(
        request,
        'reclamos/confirmacion_reclamo.html'
    )


def consulta_reclamo(request):
    return render(
        request,
        'reclamos/consulta_reclamo.html'
    )
def login_admin(request):
    return render(
        request,
        'reclamos/login.html'
    )
def menu_admin(request):
    return render(
        request,
        'reclamos/menu_admin.html'
    )

from django.shortcuts import render

def alta_usuario(request):
    return render(request, 'reclamos/alta_usuario.html')

from django.shortcuts import render
from .models import Reclamo

def panel_control(request):

    reclamos = Reclamo.objects.all()

    context = {
        'reclamos': reclamos,
        'total': reclamos.count(),
        'pendientes': reclamos.filter(estado__nombre='Pendiente').count(),
        'proceso': reclamos.filter(estado__nombre='En Proceso').count(),
        'resueltos': reclamos.filter(estado__nombre='Resuelto').count(),
    }

    return render(
    request,
    'reclamos/panel_control.html',
    context
)

from django.shortcuts import render, get_object_or_404
from .models import Reclamo, Seguimiento

def detalle_reclamo(request, id):

    reclamo = get_object_or_404(
        Reclamo,
        id=id
    )

    seguimientos = Seguimiento.objects.filter(
        reclamo=reclamo
    )

    context = {
        'reclamo': reclamo,
        'seguimientos': seguimientos
    }

    return render(
        request,
        'reclamos/detalle_reclamo.html',
        context
    )