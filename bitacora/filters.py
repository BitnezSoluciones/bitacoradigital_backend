# bitacora/filters.py

from django_filters import rest_framework as filters
from .models import Bitacora

class BitacoraFilter(filters.FilterSet):
    fecha_after = filters.DateFilter(field_name='fecha', lookup_expr='gte')
    fecha_before = filters.DateFilter(field_name='fecha', lookup_expr='lte')

    class Meta:
        model = Bitacora
        # --- CAMBIO IMPORTANTE AQUÍ ---
        # En lugar de una lista, usamos un diccionario para especificar los filtros permitidos
        fields = {
            'cliente': ['exact', 'icontains'], # Permite búsqueda exacta O que contenga el texto
            'tecnico': ['exact'],             # Para el técnico, solo búsqueda exacta por ID
        }