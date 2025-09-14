# bitacora/views.py

from rest_framework import viewsets
from .models import Bitacora
from .serializers import BitacoraSerializer

class BitacoraViewSet(viewsets.ModelViewSet):
    queryset = Bitacora.objects.all().order_by('-fecha')
    serializer_class = BitacoraSerializer