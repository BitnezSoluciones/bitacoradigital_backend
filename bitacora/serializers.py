# bitacora/serializers.py

from rest_framework import serializers
from .models import Servicio

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = ['id', 'cliente', 'fecha', 'cantidad', 'descripcion_servicio']