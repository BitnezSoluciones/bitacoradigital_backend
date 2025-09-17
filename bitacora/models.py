# bitacora/models.py

from django.db import models
from django.contrib.auth.models import User # 1. Importamos el modelo de Usuario de Django

# Modelo para el "encabezado": El cliente y la fecha general del servicio.
class Bitacora(models.Model):
    cliente = models.CharField(max_length=200)
    fecha = models.DateField()
    tecnico = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Bitácora para {self.cliente} del {self.fecha}"

# Modelo para las "líneas": Cada servicio o producto individual.
class Partida(models.Model):
    # La relación clave: Cada partida PERTENECE a UNA Bitacora.
    # on_delete=models.CASCADE significa que si se borra una Bitacora,
    # todas sus partidas asociadas también se borrarán.
    bitacora = models.ForeignKey(Bitacora, related_name='partidas', on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    descripcion = models.TextField()
    costo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"Partida de {self.cantidad} para {self.bitacora.cliente}"