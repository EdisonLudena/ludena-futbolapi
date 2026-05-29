# gestion/serializers/evento.py
from rest_framework import serializers
from gestion.models import EventoPartido, Jugador

class EventoPartidoSerializer(serializers.ModelSerializer):
    jugador_nombre = serializers.CharField(source='jugador.nombres', read_only=True)
    jugador_apellido = serializers.CharField(source='jugador.apellidos', read_only=True)
    posicion = serializers.CharField(source='jugador.posicion', read_only=True)

    class Meta:
        model = EventoPartido
        fields = [
            'id', 'jugador', 'jugador_nombre', 'jugador_apellido', 'posicion',
            'minutos_jugados', 'goles', 'asistencias', 'tarjetas_amarillas', 'tarjeta_roja'
        ]

class AddEventoSerializer(serializers.Serializer):
    jugador_id = serializers.IntegerField()
    minutos_jugados = serializers.IntegerField(min_value=0, max_value=120, default=90)
    goles = serializers.IntegerField(min_value=0, default=0)
    asistencias = serializers.IntegerField(min_value=0, default=0)
    tarjetas_amarillas = serializers.IntegerField(min_value=0, max_value=2, default=0)
    tarjeta_roja = serializers.BooleanField(default=False)

    def validate_jugador_id(self, value):
        if not Jugador.objects.filter(pk=value, is_active=True).exists():
            raise serializers.ValidationError(f"El jugador con ID {value} no existe o está inactivo.")
        return value