# bitacora/urls.py

from django.urls import path
from .views import ServicioListCreateAPIView

urlpatterns = [
    path('servicios/', ServicioListCreateAPIView.as_view(), name='servicio-list-create'), # <--- This comma is the fix!
]