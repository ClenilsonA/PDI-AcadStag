from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.decorators import role_required
from avaliacoes.models import AvaliacaoEntidade, AvaliacaoOrientador
from candidaturas.models import Candidatura
from certificados.models import Certificado
from estagios.models import Estagio
from processos.models import ProcessoEstagio


def _build_aluno_context(user):
    candidaturas = (
        Candidatura.objects.filter(aluno=user)
        .select_related("estagio", "estagio__empresa", "processo")
        .order_by("-data_candidatura")
    )

    candidaturas_aceites = candidaturas.filter(status=Candidatura.Status.ACEITE)

    return {
        "kpis": {
            "submetidas": candidaturas.filter(status=Candidatura.Status.SUBMETIDA).count(),
            "aceites": candidaturas_aceites.count(),
            "rejeitadas": candidaturas.filter(status=Candidatura.Status.REJEITADA).count(),
            "processos": ProcessoEstagio.objects.filter(candidatura__aluno=user).count(),
        },
        "ultimas_candidaturas": candidaturas[:5],
        "estagios_recentes": Estagio.objects.filter(ativo=True).order_by("-data_criacao")[:5],
        "relatorios_pendentes": [
            candidatura
            for candidatura in candidaturas_aceites
            if not hasattr(candidatura, "relatorio")
        ],
    }


def _build_empresa_context(user):
    empresa = getattr(user, "empresa", None)

    if not empresa:
        return {
            "kpis": {
                "estagios_ativos": 0,
                "candidaturas_submetidas": 0,
                "candidaturas_total": 0,
                "processos": 0,
                "avaliacoes_praticas": 0,
            },
            "meus_estagios": [],
            "ultimas_candidaturas": [],
        }

    estagios = Estagio.objects.filter(empresa=empresa).order_by("-data_criacao")

    candidaturas = (
        Candidatura.objects.filter(estagio__empresa=empresa)
        .select_related("aluno", "estagio", "processo")
        .order_by("-data_candidatura")
    )

    processos = ProcessoEstagio.objects.filter(candidatura__estagio__empresa=empresa)

    return {
        "kpis": {
            "estagios_ativos": estagios.filter(ativo=True).count(),
            "candidaturas_submetidas": candidaturas.filter(status=Candidatura.Status.SUBMETIDA).count(),
            "candidaturas_total": candidaturas.count(),
            "processos": processos.count(),
            "avaliacoes_praticas": AvaliacaoEntidade.objects.filter(
                processo__candidatura__estagio__empresa=empresa
            ).count(),
        },
        "meus_estagios": estagios[:5],
        "ultimas_candidaturas": candidaturas[:5],
    }


def _build_orientador_context(user):
    processos = (
        ProcessoEstagio.objects.filter(orientador=user)
        .select_related(
            "candidatura",
            "candidatura__aluno",
            "candidatura__estagio",
            "candidatura__estagio__empresa",
        )
        .order_by("-criado_em")
    )

    avaliacoes = (
        AvaliacaoOrientador.objects.filter(orientador=user)
        .select_related(
            "processo",
            "processo__candidatura",
            "processo__candidatura__aluno",
            "processo__candidatura__estagio",
        )
        .order_by("-criada_em")
    )

    avaliacoes_pendentes = [
        processo
        for processo in processos
        if not hasattr(processo, "avaliacao_orientador")
    ]

    return {
        "kpis": {
            "processos_atribuidos": processos.count(),
            "avaliacoes_pendentes": len(avaliacoes_pendentes),
            "avaliacoes_feitas": avaliacoes.count(),
        },
        "processos_atribuidos_lista": processos[:5],
        "avaliacoes_pendentes_lista": avaliacoes_pendentes[:5],
        "ultimas_avaliacoes": avaliacoes[:5],
    }


def _build_admin_context():
    processos = (
        ProcessoEstagio.objects.select_related(
            "candidatura",
            "candidatura__aluno",
            "candidatura__estagio",
            "candidatura__estagio__empresa",
            "orientador",
        )
        .order_by("-criado_em")
    )

    processos_pendentes_validacao = processos.filter(
        candidatura__status=Candidatura.Status.ACEITE,
        validado_servicos_academicos=False,
    )

    return {
        "kpis": {
            "processos_total": processos.count(),
            "processos_preparacao": processos.filter(
                estado=ProcessoEstagio.Estado.PREPARACAO
            ).count(),
            "processos_em_curso": processos.filter(
                estado=ProcessoEstagio.Estado.EM_CURSO
            ).count(),
            "processos_em_avaliacao": processos.filter(
                estado=ProcessoEstagio.Estado.EM_AVALIACAO
            ).count(),
            "processos_concluidos": processos.filter(
                estado=ProcessoEstagio.Estado.CONCLUIDO
            ).count(),
            "pendentes_validacao": processos_pendentes_validacao.count(),
            "certificados_emitidos": Certificado.objects.count(),
            "avaliacoes_praticas": AvaliacaoEntidade.objects.count(),
            "avaliacoes_teoricas": AvaliacaoOrientador.objects.count(),
        },
        "ultimos_processos": processos[:5],
        "processos_pendentes_validacao": processos_pendentes_validacao[:5],
    }


@login_required
@role_required("ALUNO", "EMPRESA", "ORIENTADOR", "ADMIN", message="Acesso não autorizado.")
def dashboard_view(request):
    user = request.user

    if user.role == "ALUNO":
        context = _build_aluno_context(user)
    elif user.role == "EMPRESA":
        context = _build_empresa_context(user)
    elif user.role == "ORIENTADOR":
        context = _build_orientador_context(user)
    elif user.role == "ADMIN":
        context = _build_admin_context()
    else:
        context = {}

    return render(request, "dashboard/home.html", context)