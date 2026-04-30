from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from core.decorators import role_required
from empresas.utils import get_empresa_profile
from processos.services import atualizar_estado_processo

from .forms import ProcessoAdminForm, ProcessoEmpresaForm
from .models import ProcessoEstagio


@login_required
@role_required("ADMIN", message="Acesso restrito aos serviços académicos.")
def lista_processos(request):
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

    context = {
        "processos": processos,
    }
    return render(request, "processos/lista_processos.html", context)


@login_required
@role_required("ADMIN", message="Acesso restrito aos serviços académicos.")
def detalhe_processo(request, pk):
    processo = get_object_or_404(
        ProcessoEstagio.objects.select_related(
            "candidatura",
            "candidatura__aluno",
            "candidatura__estagio",
            "candidatura__estagio__empresa",
            "orientador",
        ),
        pk=pk,
    )

    avaliacao_orientador = getattr(processo, "avaliacao_orientador", None)
    avaliacao_entidade = getattr(processo, "avaliacao_entidade", None)

    context = {
        "processo": processo,
        "avaliacao_orientador": avaliacao_orientador,
        "avaliacao_entidade": avaliacao_entidade,
    }
    return render(request, "processos/detalhe_processo.html", context)


@login_required
@role_required("ADMIN", message="Acesso restrito aos serviços académicos.")
def editar_processo(request, pk):
    processo = get_object_or_404(
        ProcessoEstagio.objects.select_related(
            "candidatura",
            "candidatura__aluno",
            "candidatura__estagio",
            "candidatura__estagio__empresa",
            "orientador",
        ),
        pk=pk,
    )

    if request.method == "POST":
        form = ProcessoAdminForm(request.POST, instance=processo)
        if form.is_valid():
            processo=form.save()
            atualizar_estado_processo(processo)
            messages.success(request, "Processo atualizado com sucesso.")
            return redirect("processos:detalhe", pk=processo.pk)
    else:
        form = ProcessoAdminForm(instance=processo)

    context = {
        "processo": processo,
        "form": form,
    }
    return render(request, "processos/editar_processo.html", context)


@login_required
@role_required("EMPRESA", message="Acesso restrito a empresas.")
def editar_processo_empresa(request, pk):
    empresa = get_empresa_profile(request.user)
    if not empresa:
        messages.error(request, "Perfil de empresa não encontrado.")
        return redirect("estagios:list")

    processo = get_object_or_404(
        ProcessoEstagio.objects.select_related(
            "candidatura",
            "candidatura__estagio",
            "candidatura__estagio__empresa",
        ),
        pk=pk,
        candidatura__estagio__empresa=empresa,
    )

    if request.method == "POST":
        form = ProcessoEmpresaForm(request.POST, instance=processo)
        if form.is_valid():
            processo=form.save()
            atualizar_estado_processo(processo)
            messages.success(request, "Dados do estágio atualizados com sucesso.")
            return redirect("candidaturas:empresa_list")
    else:
        form = ProcessoEmpresaForm(instance=processo)

    context = {
        "processo": processo,
        "form": form,
    }
    return render(request, "processos/editar_processo_empresa.html", context)


@login_required
@role_required("ORIENTADOR", message="Acesso restrito a orientadores.")
def lista_processos_orientador(request):
    processos = (
        ProcessoEstagio.objects.filter(orientador=request.user)
        .select_related(
            "candidatura",
            "candidatura__aluno",
            "candidatura__estagio",
            "candidatura__estagio__empresa",
            "orientador",
        )
        .order_by("-criado_em")
    )

    context = {
        "processos": processos,
    }
    return render(request, "processos/orientador_lista_processos.html", context)


@login_required
@role_required("ORIENTADOR", message="Acesso restrito a orientadores.")
def detalhe_processo_orientador(request, pk):
    processo = get_object_or_404(
        ProcessoEstagio.objects.select_related(
            "candidatura",
            "candidatura__aluno",
            "candidatura__estagio",
            "candidatura__estagio__empresa",
            "orientador",
        ),
        pk=pk,
        orientador=request.user,
    )

    relatorio = getattr(processo.candidatura, "relatorio", None)
    avaliacao = getattr(processo, "avaliacao_orientador", None)

    context = {
        "processo": processo,
        "relatorio": relatorio,
        "avaliacao": avaliacao,
    }
    return render(request, "processos/orientador_detalhe_processo.html", context)