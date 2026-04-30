from django.core.validators import FileExtensionValidator
from django.db import models

from candidaturas.models import Candidatura
from users.models import User


class ProcessoEstagio(models.Model):
    class Estado(models.TextChoices):
        PREPARACAO = "PREPARACAO", "Preparação"
        EM_CURSO = "EM_CURSO", "Em curso"
        EM_AVALIACAO = "EM_AVALIACAO", "Em avaliação"
        CONCLUIDO = "CONCLUIDO", "Concluído"

    candidatura = models.OneToOneField(
        Candidatura,
        on_delete=models.CASCADE,
        related_name="processo",
    )

    #  Orientador
    orientador = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="processos_orientados",
        limit_choices_to={"role": "ORIENTADOR"},
    )

    #  Supervisor (SEM login)
    supervisor_nome = models.CharField(max_length=150, blank=True)
    supervisor_email = models.EmailField(blank=True)
    supervisor_telefone = models.CharField(max_length=30, blank=True)
    supervisor_cargo = models.CharField(max_length=120, blank=True)

    #  Dados do estágio
    local_estagio = models.CharField(max_length=200, blank=True)

    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)

    #  Acordo opcional
    acordo_estagio = models.FileField(
        upload_to="acordos_estagio/",
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        null=True,
        blank=True,
    )

    #  Estado do processo
    estado = models.CharField(
        max_length=30,
        choices=Estado.choices,
        default=Estado.PREPARACAO,
    )

    #  Controlo académico
    empresa_confirmada = models.BooleanField(default=False)
    validado_servicos_academicos = models.BooleanField(default=False)

    nota_final = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
    )

    nota_publicada = models.BooleanField(default=False)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-criado_em"]

    def __str__(self):
        return f"{self.candidatura.aluno.username} - {self.candidatura.estagio.titulo}"

    #  Regras simples de negócio
    @property
    def pronto_para_iniciar(self):
        return all([
            self.candidatura.status == Candidatura.Status.ACEITE,
            self.orientador_id,
            self.supervisor_nome,
            self.data_inicio,
        ])
    
    from django.core.validators import FileExtensionValidator
    from django.db import models

    from candidaturas.models import Candidatura
    from users.models import User


class ProcessoEstagio(models.Model):
    class Estado(models.TextChoices):
        PREPARACAO = "PREPARACAO", "Preparação"
        EM_CURSO = "EM_CURSO", "Em curso"
        EM_AVALIACAO = "EM_AVALIACAO", "Em avaliação"
        CONCLUIDO = "CONCLUIDO", "Concluído"

    candidatura = models.OneToOneField(
        Candidatura,
        on_delete=models.CASCADE,
        related_name="processo",
    )

    #  Orientador
    orientador = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="processos_orientados",
        limit_choices_to={"role": "ORIENTADOR"},
    )

    #  Supervisor (SEM login)
    supervisor_nome = models.CharField(max_length=150, blank=True)
    supervisor_email = models.EmailField(blank=True)
    supervisor_telefone = models.CharField(max_length=30, blank=True)
    supervisor_cargo = models.CharField(max_length=120, blank=True)

    #  Dados do estágio
    local_estagio = models.CharField(max_length=200, blank=True)

    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)

    #  Acordo opcional
    acordo_estagio = models.FileField(
        upload_to="acordos_estagio/",
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        null=True,
        blank=True,
    )

    #  Estado do processo
    estado = models.CharField(
        max_length=30,
        choices=Estado.choices,
        default=Estado.PREPARACAO,
    )

    #  Controlo académico
    empresa_confirmada = models.BooleanField(default=False)
    validado_servicos_academicos = models.BooleanField(default=False)

    nota_final = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
    )

    nota_publicada = models.BooleanField(default=False)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-criado_em"]

    def __str__(self):
        return f"{self.candidatura.aluno.username} - {self.candidatura.estagio.titulo}"

    #  Regras simples de negócio
    @property
    def pronto_para_iniciar(self):
        return all([
            self.candidatura.status == Candidatura.Status.ACEITE,
            self.orientador_id,
            self.supervisor_nome,
            self.data_inicio,
        ])