# gestion/views/jugador.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

from gestion.models import Jugador
from gestion.serializers.jugador import JugadorSerializer
from gestion.permissions import IsCoachOrReadOnly 
from gestion.filters import JugadorFilter
from gestion.pagination import StandardPagination

class JugadorViewSet(viewsets.ModelViewSet):
    queryset = Jugador.objects.all()
    serializer_class = JugadorSerializer
    permission_classes = [IsCoachOrReadOnly]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = JugadorFilter
    search_fields = ['nombres', 'apellidos', 'categoria', 'posicion']
    ordering_fields = ['apellidos', 'categoria', 'created_at']
    ordering = ['apellidos']

    @action(detail=True, methods=['get'], url_path='partidos')
    def partidos_jugados(self, request, pk=None):
        """
        ACTUALIZADO EN ETAPA 4: Retorna la lista de partidos del equipo 
        al que pertenece este jugador de manera paginada.
        """
        from gestion.models import Partido
        from gestion.serializers.partido import PartidoSummarySerializer
        
        jugador = self.get_object()
        # Buscamos los partidos que pertenecen al mismo Coach (usuario) que registró al jugador
        qs = Partido.objects.filter(usuario=jugador.usuario, is_active=True).order_by('-fecha')
        
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(
                PartidoSummarySerializer(page, many=True).data
            )
        return Response(PartidoSummarySerializer(qs, many=True).data)

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        """Devuelve un resumen estadístico de los jugadores registrados"""
        qs = Jugador.objects.all()
        
        # Agrupación básica por categorías
        por_categoria = qs.values('categoria').annotate(total=Count('id')).order_by('-total')

        return Response({
            'total_jugadores': qs.count(),
            'activos': qs.filter(is_active=True).count(),
            'inactivos': qs.filter(is_active=False).count(),
            'resumen_categorias': list(por_categoria)
        })