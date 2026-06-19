from django.http import HttpResponse

def inicio(request):
    return HttpResponse("Bienvenido al Sistema de Reclamos")