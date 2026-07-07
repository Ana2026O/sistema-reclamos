from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



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
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True, null=True)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    estado = models.ForeignKey('Estado', on_delete=models.CASCADE)
    prioridad = models.ForeignKey('Prioridad', on_delete=models.CASCADE)

    # Campos de auditoría
    fecha_estado = models.DateTimeField(null=True, blank=True)
    fecha_prioridad = models.DateTimeField(null=True, blank=True)
    fecha_eliminacion = models.DateTimeField(null=True, blank=True)
    usuario_accion = models.CharField(max_length=100, null=True, blank=True)
    eliminado = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.pk:  # si ya existe en la base
            original = Reclamo.objects.get(pk=self.pk)
            # Si cambió el estado
            if original.estado != self.estado:
                self.fecha_estado = timezone.now()
                self.usuario_accion = str(self.usuario_accion or "sistema")
            # Si cambió la prioridad
            if original.prioridad != self.prioridad:
                self.fecha_prioridad = timezone.now()
                self.usuario_accion = str(self.usuario_accion or "sistema")
            # Si se marcó como eliminado
            if not original.eliminado and self.eliminado:
                self.fecha_eliminacion = timezone.now()
                self.usuario_accion = str(self.usuario_accion or "sistema")
        super().save(*args, **kwargs)
    def __str__(self):
        return f"REC-{self.id}"


class ReclamoEliminado(models.Model):
    reclamo = models.ForeignKey(Reclamo, on_delete=models.CASCADE)
    fecha_eliminacion = models.DateTimeField()
    usuario_accion = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.reclamo} eliminado por {self.usuario_accion}"


class Seguimiento(models.Model):

    comentario = models.TextField()

    fecha = models.DateTimeField(
        auto_now_add=True
    )

    reclamo = models.ForeignKey(
        Reclamo,
        on_delete=models.CASCADE
    )

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Seguimiento {self.id}"
        