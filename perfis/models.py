from django.db import models
from users.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=30, blank=True)
    curso = models.CharField(max_length=120, blank=True)

    orientador = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="alunos_orientados",
        limit_choices_to={"role": "ORIENTADOR"},
    )

    def __str__(self):
        return f"Perfil de {self.user.username}"