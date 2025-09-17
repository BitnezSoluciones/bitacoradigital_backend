# bitacora/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BitacoraViewSet, generar_reporte_pdf
from .views import ReporteFacturacionView

# Creamos un router y registramos nuestro ViewSet con él.
router = DefaultRouter()
router.register(r'bitacoras', BitacoraViewSet, basename='bitacora')

# Las URLs de la API ahora son generadas automáticamente por el router.
urlpatterns = [
    path('bitacoras/resumen/', ReporteFacturacionView.as_view(), name='bitacora-resumen'),
    path('bitacoras/<int:pk>/reporte/', generar_reporte_pdf, name='bitacora-reporte-pdf'),
    path('', include(router.urls)),
]