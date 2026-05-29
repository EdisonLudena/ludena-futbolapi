# gestion/serializers/jugador.py
from rest_framework import serializers
from django.db.models import Sum
from gestion.models import Jugador

class JugadorSerializer(serializers.ModelSerializer):
    total_partidos = serializers.SerializerMethodField()
    total_goles = serializers.SerializerMethodField()
    total_evaluaciones = serializers.SerializerMethodField() # 👈 NUEVO: Activado por completo
    coach_username = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = Jugador
        fields = [
            'id', 'usuario', 'coach_username', 'nombres', 'apellidos', 
            'categoria', 'posicion', 'foto_url', 'is_active', 
            'total_partidos', 'total_goles', 'total_evaluaciones', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'usuario']

    def get_total_partidos(self, obj):
        # Cuenta los partidos en los que el jugador tiene un registro de rendimiento (eventos)
        return obj.estadisticas_partidos.count()

    def get_total_goles(self, obj):
        # Suma los goles acumulados en todos sus Eventos de Partido
        resultado = obj.estadisticas_partidos.aggregate(suma=Sum('goles'))
        return resultado['suma'] or 0

    def get_total_evaluaciones(self, obj):
        # 👈 NUEVO: Cuenta cuántas evaluaciones físicas y técnicas se le han practicado a este jugador
        return obj.evaluaciones.count()

    def create(self, validated_data):
        # Asigna automáticamente al Coach logueado como el dueño/creador del jugador
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)