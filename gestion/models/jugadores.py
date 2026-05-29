# gestion/models/jugadores.py
from django.db import models
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class Jugador(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='jugadores')
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50, help_text="Ej: Sub-15, Senior, Reserva")
    posicion = models.CharField(max_length=50, help_text="Ej: Delantero, Central, Portero")
    foto_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True, help_text="Indica si el jugador sigue activo en el equipo")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Jugador'
        verbose_name_plural = 'Jugadores'
        ordering = ['apellidos', 'nombres']

    def __str__(self):
        return f"{self.apellidos}, {self.nombres} ({self.categoria})"