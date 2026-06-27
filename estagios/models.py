from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from empresas.models import Empresa


class Estagio(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    area = models.CharField(max_length=100)

    duracao_meses = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(12),
        ]
    )

    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name="estagios"
    )

    def __str__(self):
        return self.titulo