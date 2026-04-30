from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from core.decorators import role_required
from candidaturas.models import Candidatura
from processos.models import ProcessoEstagio
from processos.services import atualizar_estado_processo

from .forms import RelatorioForm
from .models import Relatorio


@login_required
@role_required("ALUNO", message="Acesso restrito a alunos.")
def aluno_relatorios(request):
    candidaturas = (
        Candidatura.objects.filter(aluno=request.user, status=Candidatura.Status.ACEITE)
        .select_related("estagio", "estagio__empresa", "processo")
        .order_by("-data_candidatura")
    )

    context = {
        "candidaturas": candidaturas,
    }
    return render(request, "relatorios/aluno_relatorios.html", context)


@login_required
@role_required("ALUNO", message="Acesso restrito a alunos.")
def upload_relatorio(request, candidatura_id):
    candidatura = get_object_or_404(
        Candidatura.objects.select_related("estagio", "estagio__empresa", "processo"),
        id=candidatura_id,
        aluno=request.user,
        status=Candidatura.Status.ACEITE,
    )

    processo = getattr(candidatura, "processo", None)

    if not processo:
        messages.error(
            request,
            "Ainda não existe processo de estágio associado a esta candidatura.",
        )
        return redirect("relatorios:aluno_list")

    estados_permitidos = [
        ProcessoEstagio.Estado.EM_CURSO,
        ProcessoEstagio.Estado.EM_AVALIACAO,
    ]

    if processo.estado not in estados_permitidos:
        messages.error(
            request,
            "Só podes submeter o relatório quando o estágio estiver em curso.",
        )
        return redirect("relatorios:aluno_list")

    relatorio, _ = Relatorio.objects.get_or_create(candidatura=candidatura)

    if request.method == "POST":
        form = RelatorioForm(request.POST, request.FILES, instance=relatorio)

        if form.is_valid():
            relatorio_guardado = form.save(commit=False)
            relatorio_guardado.estado = "PENDENTE"
            relatorio_guardado.candidatura = candidatura
            relatorio_guardado.save()

            atualizar_estado_processo(processo)

            messages.success(request, "Relatório submetido com sucesso!")
            return redirect("relatorios:aluno_list")
    else:
        form = RelatorioForm(instance=relatorio)

    context = {
        "form": form,
        "candidatura": candidatura,
        "processo": processo,
    }
    return render(request, "relatorios/upload.html", context)