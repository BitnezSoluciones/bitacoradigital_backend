# bitacora/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BitacoraViewSet

# Creamos un router y registramos nuestro ViewSet con él.
router = DefaultRouter()
router.register(r'bitacoras', BitacoraViewSet, basename='bitacora')

# Las URLs de la API ahora son generadas automáticamente por el router.
urlpatterns = [
    path('', include(router.urls)),
]