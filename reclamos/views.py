from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

from django import forms
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

from .forms import ReclamoForm, UsuarioForm
from .models import Reclamo

from django.contrib.auth.models import User

from .models import Estado, Prioridad, Seguimiento   

from .models import Categoria
from .forms import CategoriaForm
 

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from .forms import UsuarioForm

from .forms import ConsultaReclamoForm

from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncMonth
from .models import Reclamo


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
        if request.POST.get("categoria"):
         reclamo.categoria = Categoria.objects.get(id=request.POST.get("categoria"))
                
        reclamo.save()
        return redirect("panel_control")

    estados = Estado.objects.all()
    prioridades = Prioridad.objects.all()
    categorias = Categoria.objects.all()
    return render(request, 'reclamos/detalle_reclamo.html', {
        'reclamo': reclamo,
        'estados': estados,
        'prioridades': prioridades,
          'categorias': categorias,
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

def editar_reclamo(request, pk):
    reclamo = get_object_or_404(Reclamo, pk=pk)
    if request.method == "POST":
        form = EditarCategoriaReclamoForm(request.POST, instance=reclamo)
        if form.is_valid():
            form.save()
            return redirect('panel_control')
    else:
        form = EditarCategoriaReclamoForm(instance=reclamo)
    return render(request, 'editar_reclamo.html', {'form': form, 'reclamo': reclamo})

#---------------------------------------------------------------categorias


def lista_categorias(request):
    if request.method == "POST":    
        nombre = request.POST.get("nombre")
        if nombre:
            Categoria.objects.create(nombre=nombre)
            return redirect("categorias")  # redirige al listado

    categorias = Categoria.objects.all()
    return render(request, "reclamos/categorias.html", {"categorias": categorias})







def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == "POST":
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()   # ✅ guarda cambios
            return redirect("categorias")
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, "reclamos/editar_categoria.html", {"form": form, "categoria": categoria})


def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == "POST":
        categoria.delete()
        return redirect("categorias")
    return render(request, "reclamos/eliminar_categoria.html", {"categoria": categoria})





def es_admin(user):
    return user.groups.filter(name="admin").exists()


# ✅ LISTA DE USUARIOS
@login_required
@user_passes_test(es_admin)
def lista_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'reclamos/lista_usuarios.html', {'usuarios': usuarios})

# ✅ ALTA / MODIFICAR USUARIO
@login_required
@user_passes_test(es_admin)
def alta_usuario(request, pk=None):
    if pk:
        usuario = get_object_or_404(User, pk=pk)
    else:
        usuario = None

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            user = form.save(commit=False)

            # Contraseña obligatoria solo si es alta
            if not usuario and not form.cleaned_data['password']:
                return render(request, 'reclamos/alta_usuario.html', {
                    'form': form,
                    'error': 'La contraseña es obligatoria'
                })

            # Guardar contraseña si se ingresó
            if form.cleaned_data['password']:
                user.set_password(form.cleaned_data['password'])

            user.save()

            # Asignar grupo según rol
            role = form.cleaned_data.get("role")
            if role:
                try:
                    grupo = Group.objects.get(name=role)
                    user.groups.clear()
                    user.groups.add(grupo)
                except Group.DoesNotExist:
                    pass

            return redirect('lista_usuarios')
    else:
        form = UsuarioForm(instance=usuario)

    return render(request, 'reclamos/alta_usuario.html', {'form': form})

# ✅ ELIMINAR USUARIO
@login_required
@user_passes_test(es_admin)
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        usuario.delete()
        return redirect('lista_usuarios')
    return render(request, 'reclamos/eliminar_usuario.html', {'usuario': usuario})




def consulta_reclamo(request):
    resultado = None
    seguimiento = None

    if request.method == "POST":
        form = ConsultaReclamoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data["nombre_apellido"]
            referencia = form.cleaned_data["numero_referencia"]

            try:
                reclamo = Reclamo.objects.get(id=referencia)
                resultado = {
                    "numero": reclamo.id,
                    "nombre": nombre,
                    "estado": reclamo.estado.nombre,
                    "categoria": reclamo.categoria.nombre if reclamo.categoria else "Sin categoría"
                }
                seguimiento = reclamo.seguimiento_set.last()
            except Reclamo.DoesNotExist:
                resultado = {"error": "No se encontró ningún reclamo con ese número."}
    else:
        form = ConsultaReclamoForm()

    return render(
        request,
        "reclamos/consulta_reclamo.html",
        {"form": form, "resultado": resultado, "seguimiento": seguimiento}
    )

   
def estadisticas_reclamos(request):
    estadisticas = (
        Reclamo.objects
        .annotate(mes=TruncMonth('fecha_creacion'))
        .values('mes', 'estado', 'prioridad')
        .annotate(cantidad=Count('id'))
        .order_by('mes')
    )
    return render(request, 'reclamos/estadisticas.html', {'estadisticas': estadisticas})



from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from .models import Reclamo

def reclamos_pdf(request):
    reclamos = Reclamo.objects.all().order_by('-fecha_creacion')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reclamos_panel.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 16)
    p.drawString(180, height - 80, "Gestión de Reclamos")

    p.setFont("Helvetica", 12)
    y = height - 120
    for reclamo in reclamos:
        p.drawString(50, y, f"Nombre: {reclamo.nombre}")
        p.drawString(250, y, f"Teléfono: {reclamo.telefono}")
        p.drawString(400, y, f"Estado: {reclamo.estado}")
        y -= 20
        p.drawString(250, y, f"Prioridad: {reclamo.prioridad}")
        y -= 30

        if y < 100:  # salto de página si se llena
            p.showPage()
            p.setFont("Helvetica", 12)
            y = height - 100

    p.showPage()
    p.save()
    return response
