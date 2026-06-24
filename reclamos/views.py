from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django import forms
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

from .forms import ReclamoForm, UsuarioForm
from .models import Reclamo

from django.contrib.auth.models import User
from .forms import UsuarioForm

from .models import Estado, Prioridad

from .models import Estado, Prioridad, Seguimiento   


# ---------------- INICIO ----------------
def inicio(request):
    return render(request, 'reclamos/inicio.html')


# ---------------- RECLAMOS ----------------
def registrar_reclamo(request):
    if request.method == 'POST':
        form = ReclamoForm(request.POST)
        if form.is_valid():
            print("FORMULARIO VALIDO")
            reclamo = form.save(commit=False)
            from .models import Estado, Prioridad
            reclamo.usuario = User.objects.first()
            reclamo.estado = Estado.objects.get(nombre='Nuevo')
            reclamo.prioridad = Prioridad.objects.get(nombre='Media')
            reclamo.save()
            return redirect('confirmacion_reclamo', reclamo_id=reclamo.id)
        else:
            print("ERRORES DEL FORMULARIO:", form.errors)
    else:
        form = ReclamoForm()
    return render(request, 'reclamos/registrar_reclamo.html', {'form': form})


def confirmacion_reclamo(request, reclamo_id):
    reclamo = get_object_or_404(Reclamo, id=reclamo_id)
    return render(request, 'reclamos/confirmacion_reclamo.html', {'reclamo': reclamo})


def consulta_reclamo(request):
    return render(request, 'reclamos/consulta_reclamo.html')


# ---------------- LOGIN ADMIN ----------------
def login_admin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is None:
            error_msg = "Usuario o contraseña inválidos."
        elif not user.is_active:
            error_msg = "Tu cuenta está deshabilitada."
        else:
            login(request, user)
            return redirect("menu_admin")

        return render(request, "reclamos/login.html", {"error": error_msg})

    return render(request, "reclamos/login.html")




# ---------------- MENÚ ADMIN ----------------
def menu_admin(request):
    return render(request, 'reclamos/menu_admin.html')


# ---------------- PANEL DE CONTROL ----------------
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


# ------------ DETALLE RECLAMO ----------------

def detalle_reclamo(request, reclamo_id):
    reclamo = get_object_or_404(Reclamo, id=reclamo_id)
    seguimientos = reclamo.seguimiento_set.all().order_by("-fecha")   # ✅ obtener seguimientos

    if request.method == "POST":
        # Si viene un comentario nuevo
        comentario = request.POST.get("comentario")
        if comentario:
            Seguimiento.objects.create(
                reclamo=reclamo,
                usuario=request.user,   # el operador logueado
                comentario=comentario
            )
            return redirect("detalle_reclamo", reclamo_id=reclamo.id)

        # Si se cambian estado/prioridad
        if request.POST.get("estado"):
            reclamo.estado = Estado.objects.get(id=request.POST.get("estado"))
        if request.POST.get("prioridad"):
            reclamo.prioridad = Prioridad.objects.get(id=request.POST.get("prioridad"))
        reclamo.save()
        return redirect("panel_control")

    estados = Estado.objects.all()
    prioridades = Prioridad.objects.all()
    return render(request, 'reclamos/detalle_reclamo.html', {
        'reclamo': reclamo,
        'estados': estados,
        'prioridades': prioridades,
        'seguimientos': seguimientos   # ✅ pasar seguimientos al template
    })

    


# ---------------- DESCARGAR PDF ----------------
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


# ---------------- ALTA USUARIO ----------------


def alta_usuario(request, pk=None):
    if pk:
        usuario = get_object_or_404(User, pk=pk)
    else:
        usuario = None

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            user = form.save(commit=False)
            if not form.cleaned_data['password']:
                return render(request, 'reclamos/alta_usuario.html', {
                    'form': form,
                    'error': 'La contraseña es obligatoria'
                })
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login_admin')   # ✅ después de crear, vuelve al login
    else:
        form = UsuarioForm(instance=usuario)

    return render(request, 'reclamos/alta_usuario.html', {'form': form})





def reportes(request):
    return render(request, 'reclamos/reportes.html')

# ---------------- ELIMINAR RECLAMO ----------------
def eliminar_reclamo(request, reclamo_id):
    reclamo = get_object_or_404(Reclamo, id=reclamo_id)
    if request.method == "POST":   # ✅ solo elimina con POST
        reclamo.delete()
        return redirect('panel_control')
    return redirect('detalle_reclamo', reclamo_id=reclamo_id)


# ---------------- EDITAR RECLAMO ----------------
def editar_reclamo(request, reclamo_id):
    reclamo = get_object_or_404(Reclamo, id=reclamo_id)
    if request.method == 'POST':
        form = ReclamoForm(request.POST, instance=reclamo)
        if form.is_valid():
            form.save()   # ✅ guarda los cambios
            return redirect('panel_control')
    else:
        form = ReclamoForm(instance=reclamo)
    return render(request, 'reclamos/editar_reclamo.html', {'form': form, 'reclamo': reclamo})
#---------------------------------
