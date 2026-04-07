from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.decorators import role_required
from avaliacoes.models import Avaliacao
from candidaturas.models import Candidatura
from estagios.models import Estagio
from relatorios.models import Relatorio


def _build_aluno_context(user):
    candidaturas = (
        Candidatura.objects.filter(aluno=user)
        .select_related("estagio", "estagio__empresa")
        .order_by("-data_candidatura")
    )

    candidaturas_aceites = candidaturas.filter(status="ACEITE")

    return {
        "kpis": {
            "pendentes": candidaturas.filter(status="PENDENTE").count(),
            "aceites": candidaturas_aceites.count(),
            "rejeitadas": candidaturas.filter(status="REJEITADO").count(),
            "avaliadas": Avaliacao.objects.filter(candidatura__aluno=user).count(),
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
                "candidaturas_pendentes": 0,
                "candidaturas_total": 0,
                "relatorios_pendentes": 0,
            },
            "meus_estagios": [],
            "ultimas_candidaturas": [],
            "relatorios_pendentes_lista": [],
        }

    estagios = Estagio.objects.filter(empresa=empresa).order_by("-data_criacao")
    candidaturas = (
        Candidatura.objects.filter(estagio__empresa=empresa)
        .select_related("aluno", "estagio")
        .order_by("-data_candidatura")
    )
    relatorios_pendentes = (
        Relatorio.objects.filter(
            candidatura__estagio__empresa=empresa,
            estado="PENDENTE",
        )
        .select_related("candidatura", "candidatura__aluno", "candidatura__estagio")
        .order_by("-data_submissao")
    )

    return {
        "kpis": {
            "estagios_ativos": estagios.filter(ativo=True).count(),
            "candidaturas_pendentes": candidaturas.filter(status="PENDENTE").count(),
            "candidaturas_total": candidaturas.count(),
            "relatorios_pendentes": relatorios_pendentes.count(),
        },
        "meus_estagios": estagios[:5],
        "ultimas_candidaturas": candidaturas[:5],
        "relatorios_pendentes_lista": relatorios_pendentes[:5],
    }


def _build_orientador_context(user):
    candidaturas_aceites = (
        Candidatura.objects.filter(
            status="ACEITE",
            aluno__perfil__orientador=user,
        )
        .select_related("aluno", "estagio", "estagio__empresa")
        .order_by("-data_candidatura")
    )

    avaliacoes = (
        Avaliacao.objects.filter(candidatura__aluno__perfil__orientador=user)
        .select_related("candidatura", "candidatura__aluno", "candidatura__estagio")
        .order_by("-id")
    )

    avaliacoes_pendentes = [
        candidatura
        for candidatura in candidaturas_aceites
        if not hasattr(candidatura, "avaliacao")
    ]

    return {
        "kpis": {
            "avaliacoes_pendentes": len(avaliacoes_pendentes),
            "avaliacoes_feitas": avaliacoes.count(),
        },
        "avaliacoes_pendentes_lista": avaliacoes_pendentes[:5],
        "ultimas_avaliacoes": avaliacoes[:5],
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
    else:
        context = {}

    return render(request, "dashboard/home.html", context)