from django.db import models

# creando nuestro modelo de datos del sistema de reclamos

from django.contrib.auth.models import User


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


class Reclamo(models.Model):

    PRIORIDADES = [
        ('Baja', 'Baja'),
        ('Media', 'Media'),
        ('Alta', 'Alta'),
    ]

    ESTADOS = [
        ('Nuevo', 'Nuevo'),
        ('En Analisis', 'En Analisis'),
        ('En Proceso', 'En Proceso'),
        ('Resuelto', 'Resuelto'),
        ('Cerrado', 'Cerrado'),
    ]

    asunto = models.CharField(max_length=200)
    descripcion = models.TextField()

    prioridad = models.CharField(
        max_length=10,
        choices=PRIORIDADES,
        default='Media'
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='Nuevo'
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.id} - {self.asunto}"


class Comentario(models.Model):

    comentario = models.TextField()

    fecha = models.DateTimeField(auto_now_add=True)

    reclamo = models.ForeignKey(
        Reclamo,
        on_delete=models.CASCADE
    )

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Comentario {self.id}"
