from django.db import models

# Create your models here.
class Servicio(models.Model):
    #Campo para texto corto. 'max-lenght' es obligatorio.
    cliente = models.CharField(max_length=200)

    #Campo para guardar una fecha.
    fecha = models.DateField()

    #Campo para guardar números enteros
    cantidad = models.IntegerField()

    #Campo para texto largo, ideal para descripciones detalladas.
    descripcion_servicio = models.TextField()

    def __str__(self):
        return f"Servicio para {self.cliente} en fecha {self.fecha}"