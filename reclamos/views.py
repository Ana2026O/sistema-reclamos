from django.shortcuts import render

def inicio(request):
    return render(request, 'reclamos/inicio.html')

def registrar_reclamo(request):
    return render(request, 'reclamos/registrar_reclamo.html')

