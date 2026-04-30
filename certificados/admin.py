from django.contrib import admin

from .models import Certificado


@admin.register(Certificado)
class CertificadoAdmin(admin.ModelAdmin):
    list_display = (
        "processo",
        "aluno",
        "estagio",
        "emitido_por",
        "ativo",
        "emitido_em",
    )
    list_filter = (
        "ativo",
        "emitido_em",
    )
    search_fields = (
        "processo__candidatura__aluno__username",
        "processo__candidatura__aluno__email",
        "processo__candidatura__estagio__titulo",
        "processo__candidatura__estagio__empresa__nome",
    )
    readonly_fields = (
        "emitido_em",
        "atualizado_em",
    )

    def aluno(self, obj):
        if obj.processo:
            return obj.processo.candidatura.aluno.username
        return "-"

    def estagio(self, obj):
        if obj.processo:
            return obj.processo.candidatura.estagio.titulo
        return "-"

    aluno.short_description = "Aluno"
    estagio.short_description = "Estágio"