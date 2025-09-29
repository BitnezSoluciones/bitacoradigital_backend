# bitacora/views.

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from .serializers import UserSerializer # Importa el nuevo serializer
from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Bitacora
from .serializers import BitacoraSerializer
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from .filters import BitacoraFilter
from django.db.models import Sum, Count

@api_view(['GET'])
@authentication_classes([TokenAuthentication]) # <-- ESTA LÍNEA FALTABA
@permission_classes([IsAuthenticated])
def current_user_view(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

class BitacoraViewSet(viewsets.ModelViewSet):
    queryset = Bitacora.objects.all().order_by('-fecha')
    serializer_class = BitacoraSerializer
    authentication_classes = [TokenAuthentication] # Le dice que use tokens para saber quién es el usuario
    permission_classes = [IsAuthenticated]     # Le dice que solo usuarios logueados tienen permiso
    filterset_class = BitacoraFilter # Le dice a la vista que use nuestros filtros

    def perform_create(self, serializer):
        # Al crear una nueva bitácora, asigna automáticamente
        # al usuario autenticado (el técnico) al campo 'tecnico'.
        serializer.save(tecnico=self.request.user)

        def get_serializer_context(self):
        # Pasa el objeto 'request' completo al serializer.
        # Esto le da al serializer acceso al usuario que hace la petición.
            return {'request': self.request}

    def perform_create(self, serializer):
        serializer.save(tecnico=self.request.user)

def generar_reporte_pdf(request, pk):
    try:
        # Obtenemos la bitácora específica por su ID (pk)
        bitacora = Bitacora.objects.get(pk=pk)
    except Bitacora.DoesNotExist:
        return HttpResponse("Bitácora no encontrada.", status=404)

    # Cargamos la plantilla HTML que creamos
    template = get_template('bitacora/reporte_bitacora.html')

    # Creamos el "contexto", que son los datos que pasaremos a la plantilla
    context = {'bitacora': bitacora}

    # "Renderizamos" el HTML, es decir, combinamos la plantilla con los datos
    html = template.render(context)

    # Creamos un objeto PDF en la memoria de la computadora
    result = BytesIO()

    # Convertimos el HTML a PDF
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

    if not pdf.err:
        # Si no hubo errores, devolvemos el PDF como una respuesta descargable
        return HttpResponse(result.getvalue(), content_type='application/pdf')

    return HttpResponse("Error al generar el PDF.", status=500)

class ReporteFacturacionView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Usamos nuestra clase de filtros para filtrar el queryset
        filterset = BitacoraFilter(request.GET, queryset=Bitacora.objects.all())
        queryset_filtrado = filterset.qs

        # Calculamos los agregados sobre el queryset filtrado
        # Contamos el número total de partidas en las bitácoras filtradas
        total_partidas = queryset_filtrado.aggregate(
            total=Count('partidas')
        )['total']

        # Sumamos el costo de todas las partidas en las bitácoras filtradas
        costo_total = queryset_filtrado.aggregate(
            total=Sum('partidas__costo')
        )['total'] or 0.00 # Si no hay nada, el total es 0

        # Serializamos los datos de las bitácoras para incluirlos en el reporte
        serializer = BitacoraSerializer(queryset_filtrado, many=True)

        # Construimos la respuesta final
        data = {
            'total_partidas': total_partidas,
            'costo_total': f"{costo_total:.2f}", # Formateamos a 2 decimales
            'bitacoras_filtradas': serializer.data
        }
        return Response(data)