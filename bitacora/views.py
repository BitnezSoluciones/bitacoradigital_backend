# bitacora/views.py

from rest_framework import generics
from .models import Servicio
from .serializers import ServicioSerializer

# Esta única clase se encarga de:
# 1. Devolver la lista de servicios (GET)
# 2. Crear un nuevo servicio (POST)
class ServicioListCreateAPIView(generics.ListCreateAPIView):
    queryset = Servicio.objects.all().order_by('-fecha')
    serializer_class = ServicioSerializer

# NOTA: Las vistas antiguas para renderizar HTML (index, detalle, etc.)
# se han eliminado por ahora para enfocarnos en la API.
# Si las necesitas, deberían ir en una app separada.