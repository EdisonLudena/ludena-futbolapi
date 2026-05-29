# gestion/models/eventos.py
from django.db import models
from gestion.models.partidos import Partido
from gestion.models.jugadores import Jugador

class EventoPartido(models.Model):
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE, related_name='eventos')
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE, related_name='estadisticas_partidos')
    minutos_jugados = models.PositiveIntegerField(default=0)
    goles = models.PositiveIntegerField(default=0)
    asistencias = models.PositiveIntegerField(default=0)
    tarjetas_amarillas = models.PositiveIntegerField(default=0)
    tarjeta_roja = models.BooleanField(default=False)

    class Meta:
        unique_together = ('partido', 'jugador') # Evita duplicar estadísticas del mismo jugador en el partido
        verbose_name = 'Evento de Partido'
        verbose_name_plural = 'Eventos de Partidos'

    def __str__(self):
        return f"{self.jugador.apellidos} en {self.partido}"