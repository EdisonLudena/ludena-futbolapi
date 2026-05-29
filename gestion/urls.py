# gestion/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from gestion.views.health import health_check
from gestion.views.auth   import RegisterView, LogoutView
from gestion.views.user   import UserViewSet
from gestion.views.jugador import JugadorViewSet
from gestion.views.partido import PartidoViewSet
from gestion.views.evaluacion import EvaluacionViewSet
from gestion.serializers.auth import CustomTokenView

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('players', JugadorViewSet, basename='jugador')
router.register('matches', PartidoViewSet, basename='partido')
router.register('evaluations', EvaluacionViewSet, basename='evaluacion')

urlpatterns = [
    path('health/',             health_check),
    path('auth/register/',      RegisterView.as_view()),
    path('auth/login/',         CustomTokenView.as_view()),
    path('auth/token/refresh/', TokenRefreshView.as_view()),
    path('auth/token/verify/',  TokenVerifyView.as_view()),
    path('auth/logout/',        LogoutView.as_view()),
    path('', include(router.urls)),
]