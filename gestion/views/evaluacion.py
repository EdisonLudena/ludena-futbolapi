# gestion/views/evaluacion.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Max

from gestion.models import EvaluacionRendimiento
from gestion.serializers.evaluacion import EvaluacionRendimientoSerializer
from gestion.permissions import IsCoachOwnerOrStaff
from gestion.filters import EvaluacionFilter
from gestion.pagination import StandardPagination

class EvaluacionViewSet(viewsets.ModelViewSet):
    serializer_class = EvaluacionRendimientoSerializer
    permission_classes = [IsAuthenticated, IsCoachOwnerOrStaff]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = EvaluacionFilter
    ordering_fields = ['fecha_registro', 'calificacion_tecnica']
    ordering = ['-fecha_registro']

    def get_queryset(self):
        # Un coach solo ve el historial de evaluaciones de sus propios dirigidos
        if self.request.user.is_staff:
            return EvaluacionRendimiento.objects.select_related('jugador').all()
        return EvaluacionRendimiento.objects.filter(jugador__usuario=self.request.user).select_related('jugador')

    @action(detail=False, methods=['get'], url_path='promedios-plantel')
    def promedios(self, request):
        """Calcula los promedios físicos generales de tus jugadores actuales (Equivale a stats)"""
        qs = self.get_queryset()
        if not qs.exists():
            return Response({'message': 'Sin evaluaciones registradas aún para promediar.'})

        metricas = qs.aggregate(
            peso_promedio=Avg('peso_kg'),
            altura_promedio=Avg('altura_cm'),
            velocidad_promedio=Avg('velocidad_seg'),
            tecnica_promedio=Avg('calificacion_tecnica'),
            mejor_nota=Max('calificacion_tecnica')
        )

        return Response({
            'total_evaluaciones_analizadas': qs.count(),
            'peso_medio_kg': round(float(metricas['peso_promedio']), 2),
            'altura_media_cm': round(float(metricas['altura_promedio']), 1),
            'record_velocidad_sprint_seg': round(float(metricas['velocidad_promedio']), 2),
            'rendimiento_tecnico_promedio': round(float(metricas['tecnica_promedio']), 1),
            'maxima_calificacion_tecnica': metricas['mejor_nota']
        })