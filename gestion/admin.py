# gestion/admin.py
from django.contrib import admin
# 👇 Añadimos EvaluacionRendimiento a la importación de modelos
from gestion.models import Jugador, Partido, EventoPartido, EvaluacionRendimiento

# Configuración para ver los rendimientos de los jugadores en tablas dentro del partido
class EventoPartidoInline(admin.TabularInline):
    model = EventoPartido
    extra = 1


@admin.register(Jugador)
class JugadorAdmin(admin.ModelAdmin):
    list_display = ['id', 'apellidos', 'nombres', 'categoria', 'posicion', 'is_active']


@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'rival', 'fecha', 'lugar', 'resultado_final', 'usuario', 'is_active']
    list_filter = ['is_active', 'fecha']
    search_fields = ['rival', 'lugar']
    list_editable = ['resultado_final', 'is_active']
    inlines = [EventoPartidoInline] 


# 👇 NUEVO: Registro del modelo de evaluaciones físicas y técnicas
@admin.register(EvaluacionRendimiento)
class EvaluacionRendimientoAdmin(admin.ModelAdmin):
    list_display = ['id', 'jugador', 'fecha_registro', 'peso_kg', 'altura_cm', 'calificacion_tecnica']
    list_filter = ['fecha_registro', 'calificacion_tecnica']
    # Permite buscar evaluaciones escribiendo el nombre o apellido del jugador relacionado
    search_fields = ['jugador__apellidos', 'jugador__nombres']