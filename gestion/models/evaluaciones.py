# gestion/models/evaluaciones.py
from django.db import models
from gestion.models.jugadores import Jugador

class EvaluacionRendimiento(models.Model):
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE, related_name='evaluaciones')
    fecha_registro = models.DateField(auto_now_add=True)
    peso_kg = models.DecimalField(max_digits=5, decimal_places=2)
    altura_cm = models.PositiveIntegerField()
    velocidad_seg = models.DecimalField(max_digits=4, decimal_places=2, help_text="Tiempo en sprint de 100m o similar")
    calificacion_tecnica = models.PositiveIntegerField(help_text="Escala 1-100")
    notas_comentario = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['-fecha_registro']
        verbose_name = 'Evaluación de Rendimiento'
        verbose_name_plural = 'Evaluaciones de Rendimiento'

    def __str__(self):
        return f"Eval {self.jugador.apellidos} — {self.fecha_registro} (Nota: {self.calificacion_tecnica}/100)"