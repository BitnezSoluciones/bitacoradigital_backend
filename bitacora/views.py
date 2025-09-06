from django.middleware.csrf import get_token
from django.http import JsonResponse # Añade JsonResponse a tus importaciones de django.http
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from .models import Servicio #Importamos el modelo que creamos
from django.views.decorators.csrf import ensure_csrf_cookie

# Create your views here.
#Cuando renderices esta vista, asegúrate de enviar la cookie csrftoken al navegador, pase lo que pase
@ensure_csrf_cookie
def index(request):      
    #Revisa si el método de la petición es POST (si es envió el formulario)
    if request.method == 'POST':
        #Captura los datos del formulario usando el atributo 'name' de cada input
        cliente = request.POST.get('cliente')
        fecha = request.POST.get('fecha')
        cantidad = request.POST.get('cantidad')
        #Para la descripción, el 'name' en el HTMl es descripcion
        descripcion = request.POST.get('descripcion')

        #Crea el nuevo objeto Servicio y lo guarda en la DB
        Servicio.objects.create(
            cliente=cliente,
            fecha=fecha,
            cantidad=cantidad,
            descripcion_servicio = descripcion,
        )

        #Redirige a la misma pagina para ver la lista actualizada
        return redirect('index')
    
    #Si el método es GET (solo se visita la pagina), hace lo de siempre
    servicios = Servicio.objects.all().order_by('-fecha')
    contexto = {'servicios': servicios}
    return render (request, 'bitacora/index.html', contexto)

def detalle_servicio(request, servicio_id):
    #Esta función busca un Servicio por su ID. Si no lo encuentra, muestra un error 404.
    servicio = get_object_or_404(Servicio, id=servicio_id)

    #Prepara el contexto para enviar el objeto 'servicio' al template.
    contexto = {'servicio': servicio}

     # Renderiza un nuevo template y le pasa el contexto.
    return render(request, 'bitacora/detalle_servicio.html', contexto)

def editar_servicio(request, servicio_id):
     # Buscamos el servicio que se va to edit
    servicio = get_object_or_404(Servicio, id=servicio_id)
    
    # Si el usuario envía el formulario (POST request)...
    if request.method == 'POST':
        #Actualizamos los campos del objeto 'servicio' con los datos del formulario
        servicio.cliente = request.POST.get('cliente')
        servicio.fecha = request.POST.get('fecha')
        servicio.cantidad = request.POST.get('cantidad')
        servicio.descripcion_servicio = request.POST.get('descripcion')

        #Guardamos los cambios
        servicio.save()

        #Redirigimos al usuario de vuelta a la lista principal
        return redirect('index')
    
    #Si el usuario solo esta visitando la pagina (GET request)...
    #Preparamos el contexto para mostrar el formulario con los datos existentes
    contexto = {'servicio': servicio}

    #Renderiza un nuevo template y le pasa el contexto.
    return render (request, 'bitacora/editar_servicio.html', contexto)

@require_POST
def eliminar_servicio(request, servicio_id):
    #Buscamos el servicio que se va a eliminar
    servicio = get_object_or_404(Servicio, servicio_id)

    #Eliminamos el objeto de la base de datos
    servicio.delete()

    #Redirigimos al usuario de vuelta a la lista principal
    return redirect('index')

# Esta es nuestra nueva vista, específicamente para la API
def servicio_api(request):
    # 1. Obtenemos todos los servicios de la base de datos
    servicios = Servicio.objects.all().order_by('-fecha')
    
    # 2. Convertimos la lista de objetos en una lista de diccionarios
    data = list(servicios.values('id', 'cliente', 'fecha', 'cantidad', 'descripcion_servicio'))
    
    # 3. Devolvemos los datos como una respuesta JSON
    return JsonResponse(data, safe=False)

# Nueva vista para obtener el token CSRF
def get_csrf_token(request):
    # Obtenemos el token de la petición y lo enviamos como JSON
    token = get_token(request)
    return JsonResponse({'csrfToken': token})