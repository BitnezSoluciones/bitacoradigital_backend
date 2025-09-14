# bitacora/admin.py

from django.contrib import admin
# 1. Importa los NUEVOS modelos
from .models import Bitacora, Partida 

# Opcional: Esto mejora la visualización en el panel de admin
# Permite ver y añadir Partidas directamente desde la Bitácora.
class PartidaInline(admin.TabularInline):
    model = Partida
    extra = 1 # Muestra 1 campo extra para añadir partidas por defecto

class BitacoraAdmin(admin.ModelAdmin):
    inlines = [PartidaInline]

# 2. Registra los nuevos modelos en el panel de administración
admin.site.register(Bitacora, BitacoraAdmin)
admin.site.register(Partida)