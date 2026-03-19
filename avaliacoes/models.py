from django.db import models

# Create your models here.

from django.db import models
from candidaturas.models import Candidatura

class Avaliacao(models.Model):
    candidatura = models.OneToOneField(
        Candidatura,
        on_delete=models.CASCADE,
        related_name="avaliacao"
    )
    nota = models.IntegerField()
    comentario_orientador = models.TextField(blank=True)
    comentario_empresa = models.TextField(blank=True)
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação - {self.candidatura}"