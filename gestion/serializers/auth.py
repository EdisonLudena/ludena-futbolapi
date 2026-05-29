# gestion/serializers/auth.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Campos personalizados agregados al payload del JWT
        token['username']     = user.username
        token['email']        = user.email
        token['tipo_usuario'] = user.tipo_usuario
        token['is_staff']     = user.is_staff
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Respuesta JSON al hacer login exitoso
        data['user_id']      = self.user.id
        data['username']     = self.user.username
        data['email']        = self.user.email
        data['tipo_usuario'] = self.user.tipo_usuario
        data['idioma']       = self.user.idioma
        data['is_staff']     = self.user.is_staff
        return data

class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer