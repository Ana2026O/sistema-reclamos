from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


class Estado(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Prioridad(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Reclamo(models.Model):
    asunto = models.CharField(max_length=200)  # campo agregado

    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    prioridad = models.ForeignKey(Prioridad, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id} - {self.asunto}"


class Seguimiento(models.Model):
    comentario = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    reclamo = models.ForeignKey(Reclamo, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Seguimiento {self.id}"
