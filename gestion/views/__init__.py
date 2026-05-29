# gestion/views/__init__.py
from .health import health_check
from .auth import RegisterView, LogoutView
from .user import UserViewSet
from .jugador import JugadorViewSet
from .partido import PartidoViewSet
from .evaluacion import EvaluacionViewSet 