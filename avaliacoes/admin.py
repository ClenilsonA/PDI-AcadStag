from django.contrib import admin

from .models import AvaliacaoEntidade, AvaliacaoOrientador


@admin.register(AvaliacaoOrientador)
class AvaliacaoOrientadorAdmin(admin.ModelAdmin):
    list_display = (
        "processo",
        "orientador",
        "nota_teorica",
        "criada_em",
    )
    search_fields = (
        "processo__candidatura__aluno__username",
        "processo__candidatura__estagio__titulo",
        "orientador__username",
    )
    list_filter = ("criada_em",)


@admin.register(AvaliacaoEntidade)
class AvaliacaoEntidadeAdmin(admin.ModelAdmin):
    list_display = (
        "processo",
        "supervisor_nome_snapshot",
        "nota_pratica",
        "submetida_por",
        "criada_em",
    )
    search_fields = (
        "processo__candidatura__aluno__username",
        "processo__candidatura__estagio__titulo",
        "supervisor_nome_snapshot",
    )
    list_filter = ("criada_em",)