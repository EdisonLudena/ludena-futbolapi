# gestion/serializers/user.py
from rest_framework import serializers
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class RegisterSerializer(serializers.Serializer):
    username     = serializers.CharField(max_length=150)
    email        = serializers.EmailField()
    password     = serializers.CharField(min_length=8, write_only=True)
    password2    = serializers.CharField(write_only=True)
    tipo_usuario = serializers.ChoiceField(choices=Usuario.TIPO_USUARIO_CHOICES, default='Coach')
    idioma       = serializers.CharField(max_length=10, default='Español')

    def validate_username(self, value):
        if Usuario.objects.filter(username=value).exists():
            raise serializers.ValidationError('Este nombre de usuario ya está en uso.')
        return value

    def validate_email(self, value):
        if Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError('Este correo electrónico ya está registrado.')
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password2': 'Las contraseñas no coinciden.'})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        return Usuario.objects.create_user(**validated_data)


# 👇 REEMPLAZADO: Nueva versión de UserSerializer con contador de partidos y evaluaciones
class UserSerializer(serializers.ModelSerializer):
    total_partidos_creados = serializers.SerializerMethodField()
    total_evaluaciones_realizadas = serializers.SerializerMethodField()

    class Meta:
        model  = Usuario
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'tipo_usuario', 'idioma', 'is_staff', 'is_active', 'date_joined',
            'total_partidos_creados', 'total_evaluaciones_realizadas'
        ]
        read_only_fields = ['id', 'date_joined']

    def get_total_partidos_creados(self, obj):
        return obj.partidos.count()

    def get_total_evaluaciones_realizadas(self, obj):
        # Cuenta las evaluaciones hechas en todos los jugadores pertenecientes a este Coach
        from gestion.models import EvaluacionRendimiento
        return EvaluacionRendimiento.objects.filter(jugador__usuario=obj).count()


class UserProfileSerializer(serializers.ModelSerializer):
    """Vista y edición del perfil del propio usuario autenticado."""
    class Meta:
        model  = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'tipo_usuario', 'idioma']
        read_only_fields = ['id', 'tipo_usuario']

    def validate_email(self, value):
        request = self.context.get('request')
        if Usuario.objects.filter(email=value).exclude(pk=request.user.pk).exists():
            raise serializers.ValidationError('Este correo electrónico ya está en uso.')
        return value


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password     = serializers.CharField(min_length=8, write_only=True)
    new_password2    = serializers.CharField(write_only=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError('La contraseña actual es incorrecta.')
        return value

    def validate(self, data):
        if data['new_password'] != data['new_password2']:
            raise serializers.ValidationError({'new_password2': 'Las nuevas contraseñas no coinciden.'})
        return data