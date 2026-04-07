from django.db import models

from users.models import User


class Empresa(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="empresa",
        limit_choices_to={"role": "EMPRESA"},
    )
    nome = models.CharField(max_length=200)
    area = models.CharField(max_length=120, blank=True)
    contacto = models.CharField(max_length=120, blank=True)
    morada = models.CharField(max_length=200, blank=True)
    nif = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.nome