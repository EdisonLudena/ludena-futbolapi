# gestion/serializers/__init__.py
from .auth import CustomTokenSerializer, CustomTokenView
from .user import (
    RegisterSerializer,
    UserSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer,
)
from .jugador import JugadorSerializer 
from .partido import PartidoSerializer, PartidoSummarySerializer
from .evento import EventoPartidoSerializer, AddEventoSerializer
from .evaluacion import EvaluacionRendimientoSerializer