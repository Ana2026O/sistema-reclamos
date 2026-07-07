from django.contrib import admin
from .models import Categoria, Estado, Prioridad, Reclamo, Seguimiento, ReclamoEliminado

admin.site.register(Categoria)
admin.site.register(Estado)
admin.site.register(Prioridad)
admin.site.register(Reclamo)
admin.site.register(Seguimiento)
admin.site.register(ReclamoEliminado)