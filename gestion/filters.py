# gestion/filters.py
import django_filters
from gestion.models import Jugador, Partido, EventoPartido, EvaluacionRendimiento

class JugadorFilter(django_filters.FilterSet):
    apellidos = django_filters.CharFilter(lookup_expr='icontains')
    categoria = django_filters.CharFilter(lookup_expr='iexact')
    posicion = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Jugador
        fields = ['is_active', 'usuario']


class PartidoFilter(django_filters.FilterSet):
    rival = django_filters.CharFilter(lookup_expr='icontains')
    lugar = django_filters.CharFilter(lookup_expr='icontains')
    
    # Filtros de rango de tiempo (Reemplazan a price_min y price_max)
    fecha_desde = django_filters.DateTimeFilter(field_name='fecha', lookup_expr='gte')
    fecha_hasta = django_filters.DateTimeFilter(field_name='fecha', lookup_expr='lte')

    class Meta:
        model = Partido
        fields = ['is_active', 'usuario']

class EventoPartidoFilter(django_filters.FilterSet):
    # Permite filtrar por un jugador en específico o por el partido completo
    class Meta:
        model = EventoPartido
        fields = ['jugador', 'partido']


class EvaluacionFilter(django_filters.FilterSet):
    desde_fecha = django_filters.DateFilter(field_name='fecha_registro', lookup_expr='gte')
    hasta_fecha = django_filters.DateFilter(field_name='fecha_registro', lookup_expr='lte')

    class Meta:
        model = EvaluacionRendimiento
        fields = ['jugador']