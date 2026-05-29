from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    TIPO_USUARIO_CHOICES = [
        ('Coach', 'Coach'),
        ('Scout', 'Scout'),
        ('Player', 'Player'),
    ]
    tipo_usuario = models.CharField(max_length=10, choices=TIPO_USUARIO_CHOICES, default='Coach')
    idioma = models.CharField(max_length=10, default='Español')