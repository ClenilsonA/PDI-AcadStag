from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Roles(models.TextChoices):
        ALUNO = "ALUNO", "Aluno"
        EMPRESA = "EMPRESA", "Empresa"
        ORIENTADOR = "ORIENTADOR", "Orientador"
        ADMIN = "ADMIN", "Administrador"

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.ALUNO


    )
    email = models.EmailField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.username
    