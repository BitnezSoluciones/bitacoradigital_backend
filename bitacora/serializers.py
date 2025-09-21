# bitacora/serializers.py

from rest_framework import serializers
from .models import Bitacora, Partida

# Serializer para el rol de TÉCNICO (sin el campo 'costo')
class TecnicoPartidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partida
        fields = ['id', 'cantidad', 'descripcion']

# Serializer para el rol de ADMINISTRADOR (con el campo 'costo')
class AdminPartidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partida
        fields = ['id', 'cantidad', 'descripcion', 'costo']

class BitacoraSerializer(serializers.ModelSerializer):
    # La magia: decidimos qué serializer de partida usar basado en el rol del usuario
    partidas = serializers.SerializerMethodField()

    class Meta:
        model = Bitacora
        fields = ['id', 'cliente', 'fecha', 'tecnico', 'partidas']

    def get_partidas(self, obj):
        # Obtenemos el usuario que está haciendo la petición desde el "contexto"
        request = self.context.get('request')
        if request and request.user.is_staff:
            # Si es staff (admin), usa el serializer con costos
            serializer = AdminPartidaSerializer(obj.partidas.all(), many=True)
        else:
            # Si no, usa el serializer sin costos
            serializer = TecnicoPartidaSerializer(obj.partidas.all(), many=True)
        return serializer.data


    # +++ MÉTODO NUEVO Y MEJORADO PARA ACTUALIZAR +++
    def update(self, instance, validated_data):
        # Obtenemos los datos de las partidas que vienen del frontend
        partidas_data = validated_data.pop('partidas')

        # 1. Actualizamos los campos del "encabezado" (Bitacora)
        instance.cliente = validated_data.get('cliente', instance.cliente)
        instance.fecha = validated_data.get('fecha', instance.fecha)
        instance.save()

        # Obtenemos los IDs de las partidas que llegaron del frontend
        partidas_ids_actuales = [item.get('id') for item in partidas_data if item.get('id')]

        # 2. Eliminamos las partidas que ya no vienen en la petición
        partidas_viejas = Partida.objects.filter(bitacora=instance)
        partidas_viejas.exclude(id__in=partidas_ids_actuales).delete()

        # 3. Actualizamos las partidas existentes y creamos las nuevas
        for partida_data in partidas_data:
            partida_id = partida_data.get('id')
            if partida_id:
                # Si la partida tiene ID, es una actualización
                partida_existente = Partida.objects.get(id=partida_id, bitacora=instance)
                partida_existente.cantidad = partida_data.get('cantidad', partida_existente.cantidad)
                partida_existente.descripcion = partida_data.get('descripcion', partida_existente.descripcion)
                partida_existente.save()
            else:
                # Si no tiene ID, es una partida nueva que se debe crear
                Partida.objects.create(bitacora=instance, **partida_data)

        return instance