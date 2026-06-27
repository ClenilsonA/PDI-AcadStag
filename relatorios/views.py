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
        Candidatura.objects.filter(
            aluno=request.user,
            status=Candidatura.Status.ACEITE
        )
        .select_related("estagio", "estagio__empresa", "processo")
        .order_by("-data_candidatura")
    )

    return render(request, "relatorios/aluno_relatorios.html", {
        "candidaturas": candidaturas
    })


@login_required
@role_required("ALUNO", message="Acesso restrito a alunos.")
def upload_relatorio(request, candidatura_id):

    candidatura = get_object_or_404(
        Candidatura.objects.select_related(
            "estagio",
            "estagio__empresa",
            "processo"
        ),
        id=candidatura_id,
        aluno=request.user,
        status=Candidatura.Status.ACEITE,
    )

    processo = getattr(candidatura, "processo", None)

    if not processo:
        messages.error(
            request,
            "Ainda não existe processo de estágio associado."
        )
        return redirect("relatorios:aluno_list")

    # Estados permitidos
    if processo.estado not in [
        ProcessoEstagio.Estado.EM_CURSO,
        ProcessoEstagio.Estado.EM_AVALIACAO,
    ]:
        messages.error(
            request,
            "Só podes submeter o relatório quando o estágio estiver em curso."
        )
        return redirect("relatorios:aluno_list")

    # 🔥 IMPORTANTE: NÃO usar get_or_create aqui
    relatorio = Relatorio.objects.filter(candidatura=candidatura).first()

    if request.method == "POST":
        form = RelatorioForm(request.POST, request.FILES, instance=relatorio)

        if form.is_valid():
            relatorio_guardado = form.save(commit=False)

            relatorio_guardado.candidatura = candidatura
            relatorio_guardado.estado = Relatorio.Estado.PENDENTE

            # se já existir ficheiro antigo, opcional: apagar (boa prática)
            if relatorio and relatorio.ficheiro and request.FILES.get("ficheiro"):
                relatorio.ficheiro.delete(save=False)

            relatorio_guardado.save()

            atualizar_estado_processo(processo)

            messages.success(request, "Relatório submetido com sucesso!")
            return redirect("relatorios:aluno_list")

    else:
        form = RelatorioForm(instance=relatorio)

    return render(request, "relatorios/upload.html", {
        "form": form,
        "candidatura": candidatura,
        "processo": processo,
    })  