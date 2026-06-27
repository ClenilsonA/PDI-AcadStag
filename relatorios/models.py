from django.db import models
from candidaturas.models import Candidatura
import uuid
import os


def upload_relatorio_path(instance, filename):
    ext = filename.split('.')[-1]
    novo_nome = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join("relatorios/", novo_nome)


class Relatorio(models.Model):
    class Estado(models.TextChoices):
        PENDENTE = "PENDENTE", "Pendente"
        APROVADO = "APROVADO", "Aprovado"
        REJEITADO = "REJEITADO", "Rejeitado"

    candidatura = models.OneToOneField(
        Candidatura,
        on_delete=models.CASCADE,
        related_name="relatorio"
    )

    ficheiro = models.FileField(upload_to=upload_relatorio_path)

    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDENTE
    )

    data_submissao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Relatório - {self.candidatura}"