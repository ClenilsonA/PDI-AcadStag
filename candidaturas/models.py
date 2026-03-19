from django.db import models
from django.core.validators import FileExtensionValidator
from users.models import User
from estagios.models import Estagio


class Candidatura(models.Model):
    class Status(models.TextChoices):
        PENDENTE = "PENDENTE", "Pendente"
        ACEITE = "ACEITE", "Aceite"
        REJEITADO = "REJEITADO", "Rejeitado"

    aluno = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="candidaturas",
        limit_choices_to={"role": "ALUNO"},
    )

    estagio = models.ForeignKey(
        Estagio,
        on_delete=models.CASCADE,
        related_name="candidaturas"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDENTE
    )

    data_candidatura = models.DateTimeField(auto_now_add=True)

    cv = models.FileField(
        upload_to="cvs/",
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        verbose_name="CV em PDF",
        null=True,
        blank=True,
    )

    certificado_pdf = models.FileField(
    upload_to="certificados/",
    validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
    null=True,
    blank=True,
    verbose_name="Certificado em PDF"
    )

    class Meta:
        unique_together = ("aluno", "estagio")

    def __str__(self):
        return f"{self.aluno.username} -> {self.estagio.titulo} ({self.status})"