from django.urls import path
from . import views #Importamos nuestro archivo views.py

urlpatterns = [
    #Cuando alguien visite la URL raiz DE ESTA APP (''),
    #Se ejecutará la función 'index' que esta en views.py.
    path('', views.index, name='index'),
    #Nueva línea para la API
    path('api/servicios/', views.servicio_api, name='servicio_api'),
    #Nueva línea: define la ruta para la visita de detalle
    path('servicio/<int:servicio_id>/', views.detalle_servicio, name='detalle_servicio'),
    #Nueva línea: define la ruta para editar el servicio
    path('servicio/<int:servicio_id>/editar/', views.editar_servicio, name='editar_servicio'),
    #Nueva línea: defina la ruta para eliminar un servicio
    path('servicio/<int:servicio_id>/eliminar/', views.eliminar_servicio, name='eliminar_servicio'),
    #Nueva línea: defina la ruta para el envío del token
    path('api/get-csrf-token/', views.get_csrf_token, name='get_csrf_token'),
]
