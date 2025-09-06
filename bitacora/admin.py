from django.contrib import admin
from .models import Servicio #Importamos nuestro modelo que creamos antes

# Register your models here.

#Esta línea le dice a Django: "Muestra el modelo 'Servicio' en el panel de admin"
admin.site.register(Servicio)