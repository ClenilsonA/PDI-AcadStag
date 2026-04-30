from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from core.decorators import role_required
from empresas.utils import get_empresa_profile
from processos.models import ProcessoEstagio

from .forms import AvaliacaoEntidadeForm, AvaliacaoOrientadorForm


@login_required
@role_required("EMPRESA", message="Acesso restrito a empresas.")
def avaliar_estagio_empresa(request, processo_id):
    empresa = get_empresa_profile(request.user)
    if not empresa:
        messages.error(request, "Perfil de empresa não encontrado.")
        return redirect("estagios:list")

    processo = get_object_or_404(
        ProcessoEstagio.objects.select_related(
            "candidatura",
            "candidatura__aluno",
            "candidatura__estagio",
            "candidatura__estagio__empresa",
        ),
        pk=processo_id,
        candidatura__estagio__empresa=empresa,
    )

    if processo.estado == ProcessoEstagio.Estado.PREPARACAO:
        messages.error(
            request,
            "Só é possível avaliar a componente prática depois do processo estar em curso.",
        )
        return redirect("candidaturas:empresa_list")

    if not processo.supervisor_nome or not processo.local_estagio or not processo.data_inicio or not processo.data_fim:
        messages.error(
            request,
            "Antes de avaliar, é necessário definir supervisor, local e datas do estágio.",
        )
        return redirect("candidaturas:empresa_list")

    avaliacao = getattr(processo, "avaliacao_entidade", None)

    if request.method == "POST":
        form = AvaliacaoEntidadeForm(request.POST, instance=avaliacao)
        if form.is_valid():
            avaliacao_guardada = form.save(commit=False)
            avaliacao_guardada.processo = processo
            avaliacao_guardada.submetida_por = request.user
            avaliacao_guardada.supervisor_nome_snapshot = (
                processo.supervisor_nome or "Supervisor não definido"
            )
            avaliacao_guardada.save()

            messages.success(request, "Avaliação prática guardada com sucesso.")
            return redirect("candidaturas:empresa_list")
    else:
        form = AvaliacaoEntidadeForm(instance=avaliacao)

    context = {
        "processo": processo,
        "avaliacao": avaliacao,
        "form": form,
    }
    return render(request, "avaliacoes/avaliacao_entidade_form.html", context)


@login_required
@role_required("ORIENTADOR", message="Acesso restrito a orientadores.")
def avaliar_estagio_orientador(request, processo_id):
    processo = get_object_or_404(
        ProcessoEstagio.objects.select_related(
            "candidatura",
            "candidatura__aluno",
            "candidatura__estagio",
            "candidatura__estagio__empresa",
            "orientador",
        ),
        pk=processo_id,
        orientador=request.user,
    )

    relatorio = getattr(processo.candidatura, "relatorio", None)

    if not relatorio:
        messages.error(
            request,
            "Só é possível avaliar depois de o aluno submeter o relatório final.",
        )
        return redirect("processos:orientador_detalhe", pk=processo.pk)

    avaliacao = getattr(processo, "avaliacao_orientador", None)

    if request.method == "POST":
        form = AvaliacaoOrientadorForm(request.POST, instance=avaliacao)
        if form.is_valid():
            avaliacao_guardada = form.save(commit=False)
            avaliacao_guardada.processo = processo
            avaliacao_guardada.orientador = request.user
            avaliacao_guardada.save()

            messages.success(request, "Avaliação teórica guardada com sucesso.")
            return redirect("processos:orientador_detalhe", pk=processo.pk)
    else:
        form = AvaliacaoOrientadorForm(instance=avaliacao)

    context = {
        "processo": processo,
        "avaliacao": avaliacao,
        "form": form,
    }
    return render(request, "avaliacoes/avaliacao_orientador_form.html", context)