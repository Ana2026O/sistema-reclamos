from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import ReclamoForm
from .models import Reclamo
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from django.contrib.auth import authenticate, login   # ✅ IMPORTANTE
from django.shortcuts import render, redirect




def inicio(request):
    return render(request, 'reclamos/inicio.html')


def registrar_reclamo(request):

    if request.method == 'POST':

        form = ReclamoForm(request.POST)

        if form.is_valid():

            print("FORMULARIO VALIDO")

            reclamo = form.save(commit=False)

            from django.contrib.auth.models import User
            from .models import Estado, Prioridad

            reclamo.usuario = User.objects.first()

            reclamo.estado = Estado.objects.get(
                nombre='Nuevo'
            )

            reclamo.prioridad = Prioridad.objects.get(
                nombre='Media'
            )

            reclamo.save()

            return redirect('confirmacion_reclamo', reclamo_id=reclamo.id)

        else:

            print("ERRORES DEL FORMULARIO:")
            print(form.errors)

    else:

        form = ReclamoForm()

    return render(
        request,
        'reclamos/registrar_reclamo.html',
        {'form': form}
    )


def confirmacion_reclamo(request, reclamo_id):
    reclamo = get_object_or_404(Reclamo, id=reclamo_id)
    return render(
        request,
        'reclamos/confirmacion_reclamo.html',
        {'reclamo': reclamo}
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


def alta_usuario(request):
    return render(
        request,
        'reclamos/alta_usuario.html'
    )


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


# ✅ Vista corregida para detalle de reclamo
def detalle_reclamo(request, reclamo_id):
    reclamo = get_object_or_404(Reclamo, id=reclamo_id)
    return render(
        request,
        'reclamos/detalle_reclamo.html',
        {'reclamo': reclamo}
    )

def inicio(request):
    return render(request, 'reclamos/inicio.html')

def registrar_reclamo(request):
    if request.method == 'POST':
        form = ReclamoForm(request.POST)
        if form.is_valid():
            print("FORMULARIO VALIDO")
            reclamo = form.save(commit=False)

            from django.contrib.auth.models import User
            from .models import Estado, Prioridad

            reclamo.usuario = User.objects.first()
            reclamo.estado = Estado.objects.get(nombre='Nuevo')
            reclamo.prioridad = Prioridad.objects.get(nombre='Media')

            reclamo.save()
            return redirect('confirmacion_reclamo', reclamo_id=reclamo.id)
        else:
            print("ERRORES DEL FORMULARIO:")
            print(form.errors)
    else:
        form = ReclamoForm()
    return render(request, 'reclamos/registrar_reclamo.html', {'form': form})

def confirmacion_reclamo(request, reclamo_id):
    reclamo = get_object_or_404(Reclamo, id=reclamo_id)
    return render(request, 'reclamos/confirmacion_reclamo.html', {'reclamo': reclamo})

def consulta_reclamo(request):
    return render(request, 'reclamos/consulta_reclamo.html')

def login_admin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("menu_admin")   # redirige al menú
        else:
            return render(request, "reclamos/login.html", {"form": {"errors": True}})
    return render(request, "reclamos/login.html")

def menu_admin(request):
    return render(request, 'reclamos/menu_admin.html')

def alta_usuario(request):
    return render(request, 'reclamos/alta_usuario.html')

def panel_control(request):
    reclamos = Reclamo.objects.all()
    context = {
        'reclamos': reclamos,
        'total': reclamos.count(),
        'pendientes': reclamos.filter(estado__nombre='Pendiente').count(),
        'proceso': reclamos.filter(estado__nombre='En Proceso').count(),
        'resueltos': reclamos.filter(estado__nombre='Resuelto').count(),
    }
    return render(request, 'reclamos/panel_control.html', context)

def detalle_reclamo(request, reclamo_id):
    reclamo = get_object_or_404(Reclamo, id=reclamo_id)
    return render(request, 'reclamos/detalle_reclamo.html', {'reclamo': reclamo})

# ✅ Vista PDF
def descargar_pdf(request, reclamo_id):
    reclamo = get_object_or_404(Reclamo, id=reclamo_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reclamo_{reclamo.id}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 16)
    p.drawString(2*cm, height - 2*cm, "Sistema de Reclamos - Confirmación")
    p.line(2*cm, height - 2.2*cm, width - 2*cm, height - 2.2*cm)

    p.setFont("Helvetica", 12)
    p.drawString(2*cm, height - 3*cm, f"Reclamo N°: {reclamo.id}")
    p.drawString(2*cm, height - 4*cm, f"Fecha: {reclamo.fecha_creacion.strftime('%d/%m/%Y %H:%M')}")
    p.drawString(2*cm, height - 5*cm, f"Categoría: {reclamo.categoria}")
    p.drawString(2*cm, height - 6*cm, f"Estado: {reclamo.estado}")
    p.drawString(2*cm, height - 7*cm, f"Prioridad: {reclamo.prioridad}")

    p.setFont("Helvetica", 12)
    p.drawString(2*cm, height - 8*cm, "Descripción:")
    text_obj = p.beginText(2*cm, height - 9*cm)
    text_obj.setFont("Helvetica", 11)
    text_obj.textLines(reclamo.descripcion)
    p.drawText(text_obj)

    p.setFont("Helvetica-Oblique", 10)
    p.drawString(2*cm, 2*cm, "Este documento fue generado automáticamente por el sistema de reclamos.")

    p.showPage()
    p.save()

    return response