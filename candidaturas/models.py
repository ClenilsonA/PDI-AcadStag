import os
import uuid

from django.core.validators import FileExtensionValidator
from django.db import models

from estagios.models import Estagio
from users.models import User


def upload_cv_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    return os.path.join("candidaturas/cv", f"{uuid.uuid4().hex}{ext}")


def upload_comprovativo_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    return os.path.join("candidaturas/comprovativos", f"{uuid.uuid4().hex}{ext}")


class Candidatura(models.Model):
    class Status(models.TextChoices):
        SUBMETIDA = "SUBMETIDA", "Submetida"
        ACEITE = "ACEITE", "Aceite"
        REJEITADA = "REJEITADA", "Rejeitada"

    aluno = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="candidaturas",
        limit_choices_to={"role": "ALUNO"},
    )

    estagio = models.ForeignKey(
        Estagio,
        on_delete=models.CASCADE,
        related_name="candidaturas",
    )

    cv = models.FileField(
        upload_to=upload_cv_path,
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        null=True,
        blank=True,
    )

    comprovativo_frequencia = models.FileField(
        upload_to=upload_comprovativo_path,
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SUBMETIDA,
    )

    data_candidatura = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("aluno", "estagio")
        ordering = ["-data_candidatura"]

    def __str__(self):
        return f"{self.aluno.username} -> {self.estagio.titulo}"