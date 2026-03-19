from django.db import models
from candidaturas.models import Candidatura
from users.models import User


class Certificado(models.Model):
    candidatura = models.OneToOneField(
        Candidatura,
        on_delete=models.CASCADE,
        related_name="certificado"
    )
    orientador = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "ORIENTADOR"},
        related_name="certificados_emitidos"
    )
    data_emissao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Certificado - {self.candidatura.aluno.username} - {self.candidatura.estagio.titulo}"
