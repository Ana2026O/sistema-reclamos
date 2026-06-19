from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Categoria, Reclamo, Comentario

admin.site.register(Categoria)
admin.site.register(Reclamo)
admin.site.register(Comentario)