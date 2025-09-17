"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include #!Añadimos,'include'!
from rest_framework.authtoken import views # <-- 1. IMPORTA la vista de tokens

urlpatterns = [
    path('admin/', admin.site.urls),
    # Asegúrate de que esta línea apunte a 'bitacora.urls'
    path('api/', include('bitacora.urls')),
    # Al hacer un POST a /api-token-auth/ con 'username' y 'password',
    # devolverá el token del usuario.
    path('api-token-auth/', views.obtain_auth_token, name='api_token_auth'),
]
