# bitacora/serializers.py

from rest_framework import serializers
from .models import Bitacora, Partida

class PartidaSerializer(serializers.ModelSerializer):
    # Añadimos 'id' y lo hacemos de solo lectura para las actualizaciones
    id = serializers.IntegerField(read_only=True, required=False)
    class Meta:
        model = Partida
        fields = ['id', 'cantidad', 'descripcion']

class BitacoraSerializer(serializers.ModelSerializer):
    partidas = PartidaSerializer(many=True)

    class Meta:
        model = Bitacora
        fields = ['id', 'cliente', 'fecha', 'partidas']

    # El método create que ya teníamos
    def create(self, validated_data):
        partidas_data = validated_data.pop('partidas')
        bitacora = Bitacora.objects.create(**validated_data)
        for partida_data in partidas_data:
            Partida.objects.create(bitacora=bitacora, **partida_data)
        return bitacora

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