from django.contrib import admin
from django.utils import timezone
from .models import Categoria, Estado, Prioridad, Reclamo, Seguimiento, ReclamoEliminado

class ReclamoAdmin(admin.ModelAdmin):
    def delete_model(self, request, obj):
        ReclamoEliminado.objects.create(
            reclamo=obj,
            fecha_eliminacion=timezone.now(),
            usuario_accion=request.user.username if request.user.is_authenticated else "Anónimo"
        )
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            ReclamoEliminado.objects.create(
                reclamo=obj,
                fecha_eliminacion=timezone.now(),
                usuario_accion=request.user.username if request.user.is_authenticated else "Anónimo"
            )
        super().delete_queryset(request, queryset)

# Registrar modelos en el admin (una sola vez cada uno)
admin.site.register(Categoria)
admin.site.register(Estado)
admin.site.register(Prioridad)
admin.site.register(Reclamo, ReclamoAdmin)  # Reclamo con auditoría
admin.site.register(Seguimiento)
admin.site.register(ReclamoEliminado)
