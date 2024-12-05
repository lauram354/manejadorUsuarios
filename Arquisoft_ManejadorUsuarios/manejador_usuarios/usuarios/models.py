from django.db import models

class Institucion(models.Model):
    nombre = models.CharField(max_length=50)
    logo = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    usuario = models.CharField(max_length=50)
    correo = models.EmailField(max_length=255)
    nombre = models.CharField(max_length=50)
    contrasenia = models.CharField(max_length=255)
    rol = models.CharField(max_length=50)
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)  # Relación con la institución

    def __str__(self):
        return self.nombre
