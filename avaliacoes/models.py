from django.conf import settings
from django.db import models

from processos.models import ProcessoEstagio


class AvaliacaoOrientador(models.Model):
    processo = models.OneToOneField(
        ProcessoEstagio,
        on_delete=models.CASCADE,
        related_name="avaliacao_orientador",
    )

    orientador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="avaliacoes_orientador",
    )

    nota_teorica = models.DecimalField(max_digits=4, decimal_places=2)
    comentario = models.TextField(blank=True)

    criada_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-criada_em"]

    def __str__(self):
        return f"Avaliação do orientador - {self.processo}"


class AvaliacaoEntidade(models.Model):
    processo = models.OneToOneField(
        ProcessoEstagio,
        on_delete=models.CASCADE,
        related_name="avaliacao_entidade",
    )

    submetida_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="avaliacoes_entidade_submetidas",
    )

    supervisor_nome_snapshot = models.CharField(max_length=150)

    nota_pratica = models.DecimalField(max_digits=4, decimal_places=2)
    comentario = models.TextField(blank=True)

    criada_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-criada_em"]

    def __str__(self):
        return f"Avaliação prática - {self.processo}"