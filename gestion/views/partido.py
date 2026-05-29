# gestion/views/partido.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count

# Se importan los nuevos modelos, serializadores y el permiso IsOwnerOrStaff
from gestion.models import Partido, EventoPartido, Jugador
from gestion.serializers.partido import PartidoSerializer, PartidoSummarySerializer
from gestion.serializers.evento import EventoPartidoSerializer, AddEventoSerializer
from gestion.permissions import IsOwnerOrStaff, IsCoachOrReadOnly
from gestion.filters import PartidoFilter
from gestion.pagination import StandardPagination

class PartidoViewSet(viewsets.ModelViewSet):
    serializer_class = PartidoSerializer
    # Se actualizan los permisos: Debe estar autenticado y ser el dueño o administrador
    permission_classes = [IsAuthenticated, IsOwnerOrStaff]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PartidoFilter
    search_fields = ['rival', 'lugar', 'usuario__username']
    ordering_fields = ['fecha', 'rival']
    ordering = ['-fecha']

    def get_queryset(self):
        """
        Filtra el queryset para que el Coach común solo vea sus partidos creados,
        mientras que el Staff administrativo pueda verlos todos.
        """
        if self.request.user.is_staff:
            return Partido.objects.select_related('usuario').prefetch_related('eventos__jugador').all()
        return Partido.objects.filter(usuario=self.request.user).prefetch_related('eventos__jugador')

    def perform_create(self, serializer):
        """Asigna automáticamente el usuario logueado como el coach del partido"""
        serializer.save(usuario=self.request.user)

    @action(
        detail=True, 
        methods=['post'], 
        permission_classes=[IsAuthenticated, IsOwnerOrStaff], 
        url_path='finalizar'
    )
    def finalizar_partido(self, request, pk=None):
        """Registra el marcador definitivo del encuentro (Equivale a restock)"""
        partido = self.get_object()
        resultado = request.data.get('resultado_final')
        
        if not resultado or "-" not in resultado:
            return Response(
                {'error': 'Debe proveer un formato de resultado válido (Ej: "2-1").'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        partido.resultado_final = resultado
        partido.save(update_fields=['resultado_final'])
        return Response({
            'id': partido.id,
            'rival': partido.rival,
            'resultado_final': partido.resultado_final,
            'status': 'Partido finalizado y guardado.'
        })

    @action(detail=True, methods=['post'], url_path='registrar-rendimiento')
    def registrar_rendimiento(self, request, pk=None):
        """Añade o actualiza la actuación de un jugador en este partido (Equivale a add-item)"""
        partido = self.get_object()
        
        serializer = AddEventoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        jugador_id = serializer.validated_data['jugador_id']
        jugador = Jugador.objects.get(pk=jugador_id)

        # Crea el evento o lo actualiza si ya existía para ese jugador en el partido
        evento, created = EventoPartido.objects.get_or_create(
            partido=partido,
            jugador=jugador,
            defaults={
                'minutos_jugados': serializer.validated_data['minutos_jugados'],
                'goles': serializer.validated_data['goles'],
                'asistencias': serializer.validated_data['asistencias'],
                'tarjetas_amarillas': serializer.validated_data['tarjetas_amarillas'],
                'tarjeta_roja': serializer.validated_data['tarjeta_roja']
            }
        )

        if not created:
            evento.minutos_jugados = serializer.validated_data['minutos_jugados']
            evento.goles = serializer.validated_data['goles']
            evento.asistencias = serializer.validated_data['asistencias']
            evento.tarjetas_amarillas = serializer.validated_data['tarjetas_amarillas']
            evento.tarjeta_roja = serializer.validated_data['tarjeta_roja']
            evento.save()

        return Response(PartidoSerializer(partido).data)

    @action(detail=True, methods=['post'], url_path='confirmar')
    def confirmar(self, request, pk=None):
        """Bloquea el partido confirmando que el marcador ya fue definido (Equivale a confirm)"""
        partido = self.get_object()
        if not partido.resultado_final:
            return Response(
                {'error': 'No se puede confirmar un partido sin antes establecer su resultado_final.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({'message': 'Partido confirmado y cerrado.', 'partido': PartidoSerializer(partido).data})

    @action(
        detail=False, 
        methods=['get'], 
        permission_classes=[AllowAny], 
        url_path='proximos'
    )
    def proximos_partidos(self, request):
        """Lista los partidos planificados que aún no se han jugado (Equivale a available)"""
        # Se cambia self.get_queryset() por Partido.objects directamente para evitar que el filtro de Coach rompa la vista pública
        qs = self.filter_queryset(
            Partido.objects.filter(resultado_final__isnull=True, is_active=True)
        )
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(
                PartidoSummarySerializer(page, many=True).data
            )
        return Response(PartidoSummarySerializer(qs, many=True).data)

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        """Métricas colectivas globales de rendimiento (Goles, asistencias, tarjetas)"""
        eventos = EventoPartido.objects.all()
        partidos = Partido.objects.all()

        totales = eventos.aggregate(
            goles_totales=Sum('goles'),
            asistencias_totales=Sum('asistencias'),
            amarillas_totales=Sum('tarjetas_amarillas')
        )

        return Response({
            'total_partidos_registrados': partidos.count(),
            'goles_anotados_club': totales['goles_totales'] or 0, # Corregido para que no busque una llave inexistente
            'asistencias_totales': totales['asistencias_totales'] or 0,
            'tarjetas_amarillas_recibidas': totales['amarillas_totales'] or 0,
            'expulsiones': eventos.filter(tarjeta_roja=True).count()
        })