from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings

class Perfil(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=30, blank=True)
    curso = models.CharField(max_length=120, blank=True)  # usado no ALUNO

    def __str__(self):
        return f"Perfil de {self.user.username}"