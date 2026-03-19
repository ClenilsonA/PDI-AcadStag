from django.shortcuts import render

# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from estagios.models import Estagio
from candidaturas.models import Candidatura
from relatorios.models import Relatorio
from avaliacoes.models import Avaliacao

@login_required
def dashboard_view(request):
    user = request.user
    ctx = {}

    # ---------------- ALUNO ----------------
    if user.role == "ALUNO":
        minhas = Candidatura.objects.filter(aluno=user)

        ctx["kpis"] = {
            "pendentes": minhas.filter(status="PENDENTE").count(),
            "aceites": minhas.filter(status="ACEITE").count(),
            "rejeitadas": minhas.filter(status="REJEITADO").count(),
            "avaliadas": Avaliacao.objects.filter(candidatura__aluno=user).count(),
        }

        ctx["ultimas_candidaturas"] = minhas.order_by("-data_candidatura")[:5]
        ctx["estagios_recentes"] = Estagio.objects.filter(ativo=True).order_by("-data_criacao")[:5]

        # relatórios pendentes = candidaturas aceites sem relatório
        aceites_ids = minhas.filter(status="ACEITE").values_list("id", flat=True)
        ctx["relatorios_pendentes"] = [c for c in minhas.filter(status="ACEITE") if not hasattr(c, "relatorio")]

    # ---------------- EMPRESA ----------------
    elif user.role == "EMPRESA":
        meus_estagios = Estagio.objects.filter(empresa=user.empresa)

        candidaturas = Candidatura.objects.filter(estagio__empresa=user.empresa)

        ctx["kpis"] = {
            "estagios_ativos": meus_estagios.filter(ativo=True).count(),
            "candidaturas_pendentes": candidaturas.filter(status="PENDENTE").count(),
            "candidaturas_total": candidaturas.count(),
            "relatorios_pendentes": Relatorio.objects.filter(candidatura__estagio__empresa=user.empresa, estado="PENDENTE").count(),
        }

        ctx["meus_estagios"] = meus_estagios.order_by("-data_criacao")[:5]
        ctx["ultimas_candidaturas"] = candidaturas.order_by("-data_candidatura")[:5]
        ctx["relatorios_pendentes_lista"] = Relatorio.objects.filter(
            candidatura__estagio__empresa=user.empresa,
            estado="PENDENTE"
        ).order_by("-data_submissao")[:5]

    # ---------------- ORIENTADOR ----------------
    else:
        # se no teu projeto o orientador vê avaliações via candidaturas aceites,
        # mostramos tudo pendente (candidaturas aceites sem avaliação)
        aceites = Candidatura.objects.filter(status="ACEITE")

        pendentes = [c for c in aceites if not hasattr(c, "avaliacao")]
        feitas = Avaliacao.objects.all()

        ctx["kpis"] = {
            "avaliacoes_pendentes": len(pendentes),
            "avaliacoes_feitas": feitas.count(),
        }

        ctx["avaliacoes_pendentes_lista"] = pendentes[:5]
        ctx["ultimas_avaliacoes"] = feitas.order_by("-id")[:5]

    return render(request, "dashboard/home.html", ctx)