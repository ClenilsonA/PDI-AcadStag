from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from core.decorators import role_required
from candidaturas.models import Candidatura
from empresas.utils import get_empresa_profile

from .forms import RelatorioForm
from .models import Relatorio


@login_required
@role_required("ALUNO", message="Acesso restrito a alunos.")
def aluno_relatorios(request):
    candidaturas = (
        Candidatura.objects.filter(aluno=request.user, status="ACEITE")
        .select_related("estagio", "estagio__empresa")
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
        Candidatura.objects.select_related("estagio", "estagio__empresa"),
        id=candidatura_id,
        aluno=request.user,
        status="ACEITE",
    )

    relatorio, _ = Relatorio.objects.get_or_create(candidatura=candidatura)

    if request.method == "POST":
        form = RelatorioForm(request.POST, request.FILES, instance=relatorio)

        if form.is_valid():
            relatorio_guardado = form.save(commit=False)
            relatorio_guardado.estado = "PENDENTE"
            relatorio_guardado.candidatura = candidatura
            relatorio_guardado.save()

            messages.success(request, "Relatório submetido com sucesso!")
            return redirect("relatorios:aluno_list")
    else:
        form = RelatorioForm(instance=relatorio)

    context = {
        "form": form,
        "candidatura": candidatura,
    }
    return render(request, "relatorios/upload.html", context)


@login_required
@role_required("EMPRESA", message="Acesso restrito a empresas.")
def empresa_relatorios(request):
    empresa = get_empresa_profile(request.user)
    if not empresa:
        messages.error(request, "Perfil de empresa não encontrado.")
        return redirect("estagios:list")

    relatorios = (
        Relatorio.objects.filter(candidatura__estagio__empresa=empresa)
        .select_related("candidatura", "candidatura__aluno", "candidatura__estagio")
        .order_by("-data_submissao")
    )

    context = {
        "relatorios": relatorios,
    }
    return render(request, "relatorios/empresa_relatorios.html", context)


@login_required
@role_required("EMPRESA", message="Acesso restrito a empresas.")
def alterar_estado_relatorio(request, pk, novo_estado):
    empresa = get_empresa_profile(request.user)
    if not empresa:
        messages.error(request, "Perfil de empresa não encontrado.")
        return redirect("estagios:list")

    estados_validos = {"APROVADO", "REJEITADO", "PENDENTE"}
    if novo_estado not in estados_validos:
        messages.error(request, "Estado inválido.")
        return redirect("relatorios:empresa_list")

    relatorio = get_object_or_404(
        Relatorio,
        pk=pk,
        candidatura__estagio__empresa=empresa,
    )

    relatorio.estado = novo_estado
    relatorio.save(update_fields=["estado"])

    messages.success(request, f"Relatório atualizado para {novo_estado}.")
    return redirect("relatorios:empresa_list")