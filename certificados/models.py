import os
import uuid

from django.conf import settings
from django.db import models

from processos.models import ProcessoEstagio


def upload_certificado_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    return os.path.join("certificados", f"{uuid.uuid4().hex}{ext}")


class Certificado(models.Model):
    processo = models.OneToOneField(
        ProcessoEstagio,
        on_delete=models.CASCADE,
        related_name="certificado",
        null=True,
        blank=True,
    )

    ficheiro = models.FileField(
        upload_to=upload_certificado_path,
        null=True,
        blank=True,
    )

    emitido_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="certificados_emitidos",
        limit_choices_to={"role": "ADMIN"},
    )

    observacoes = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)

    emitido_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-emitido_em"]

    def __str__(self):
        if self.processo:
            aluno = self.processo.candidatura.aluno.username
            estagio = self.processo.candidatura.estagio.titulo
            return f"Certificado - {aluno} - {estagio}"

        return "Certificado sem processo associado"