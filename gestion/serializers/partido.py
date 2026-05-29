# gestion/serializers/partido.py
from rest_framework import serializers
from gestion.models import Partido
from gestion.serializers.user import UserSerializer

class PartidoSummarySerializer(serializers.ModelSerializer):
    """Vista simplificada de partidos para listas rápidas."""
    disputado = serializers.BooleanField(read_only=True)

    class Meta:
        model = Partido
        fields = ['id', 'rival', 'fecha', 'resultado_final', 'disputado']


class PartidoSerializer(serializers.ModelSerializer):
    coach = UserSerializer(source='usuario', read_only=True)
    disputado = serializers.SerializerMethodField()

    class Meta:
        model = Partido
        fields = [
            'id', 'rival', 'fecha', 'lugar', 'resultado_final', 
            'disputado', 'is_active', 'coach', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_disputado(self, obj):
        return obj.disputado

    def validate_rival(self, value):
        # 1. Verificamos que no sea None y limpiamos espacios antes de medir su longitud
        if not value or len(value.strip()) < 3:
            raise serializers.ValidationError('El nombre del rival debe tener al menos 3 caracteres.')
        return value