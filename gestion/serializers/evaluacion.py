# gestion/serializers/evaluacion.py
from rest_framework import serializers
from gestion.models import EvaluacionRendimiento, Jugador

class EvaluacionRendimientoSerializer(serializers.ModelSerializer):
    jugador_apellido = serializers.CharField(source='jugador.apellidos', read_only=True)
    jugador_nombre = serializers.CharField(source='jugador.nombres', read_only=True)

    class Meta:
        model = EvaluacionRendimiento
        fields = [
            'id', 'jugador', 'jugador_nombre', 'jugador_apellido', 'fecha_registro',
            'peso_kg', 'altura_cm', 'velocidad_seg', 'calificacion_tecnica', 'notas_comentario'
        ]
        read_only_fields = ['id', 'fecha_registro']

    def validate_calificacion_tecnica(self, value):
        if value < 1 or value > 100:
            raise serializers.ValidationError("La calificación técnica debe estar estrictamente en el rango de 1 a 100.")
        return value

    def validate_peso_kg(self, value):
        if value <= 0:
            raise serializers.ValidationError("El peso debe ser una cantidad positiva.")
        return value
        
    def validate_jugador(self, value):
        # Regla de oro: No puedes evaluar un jugador que pertenece a otro Coach
        request = self.context.get('request')
        if request and value.usuario != request.user and not request.user.is_staff:
            raise serializers.ValidationError("No tienes permiso para registrar evaluaciones sobre un jugador que no manejas.")
        return value