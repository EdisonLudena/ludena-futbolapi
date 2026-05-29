# gestion/models/partidos.py
from django.db import models
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class Partido(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='partidos')
    rival = models.CharField(max_length=150)
    fecha = models.DateTimeField()
    lugar = models.CharField(max_length=150)
    resultado_final = models.CharField(max_length=20, blank=True, null=True, help_text="Ej: 3-1")
    is_active = models.BooleanField(default=True, help_text="Permite cancelar o suspender lógicamente el partido")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha'] # Los partidos más recientes se muestran primero

    def __str__(self):
        return f"Vs {self.rival} - {self.fecha.strftime('%d/%m/%Y')}"

    @property
    def disputado(self):
        """Saber si el partido ya concluyó (si tiene resultado registrado)"""
        return self.resultado_final is not None and self.resultado_final != ""