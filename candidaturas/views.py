from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from core.decorators import role_required
from empresas.utils import get_empresa_profile
from estagios.models import Estagio

from .forms import CandidaturaForm
from .models import Candidatura


@login_required
@role_required("ALUNO", message="Apenas alunos podem candidatar-se.")
def criar_candidatura(request, estagio_id):
    estagio = get_object_or_404(Estagio, id=estagio_id, ativo=True)

    candidatura_existente = Candidatura.objects.filter(
        aluno=request.user,
        estagio=estagio,
    ).exists()
    if candidatura_existente:
        messages.info(request, "Já existe uma candidatura para este estágio.")
        return redirect("candidaturas:minhas")

    if request.method == "POST":
        form = CandidaturaForm(request.POST, request.FILES)

        if form.is_valid():
            candidatura = form.save(commit=False)
            candidatura.aluno = request.user
            candidatura.estagio = estagio
            candidatura.save()

            messages.success(request, "Candidatura submetida com sucesso!")
            return redirect("candidaturas:minhas")
    else:
        form = CandidaturaForm()

    context = {
        "form": form,
        "estagio": estagio,
    }
    return render(request, "candidaturas/candidatura_form.html", context)


@login_required
@role_required("ALUNO", message="Apenas alunos têm candidaturas.")
def minhas_candidaturas(request):
    candidaturas = (
        Candidatura.objects.filter(aluno=request.user)
        .select_related("estagio", "estagio__empresa")
        .order_by("-data_candidatura")
    )

    context = {
        "candidaturas": candidaturas,
    }
    return render(request, "candidaturas/minhas_candidaturas.html", context)


@login_required
@role_required("EMPRESA", message="Acesso restrito a empresas.")
def empresa_candidaturas(request):
    empresa = get_empresa_profile(request.user)
    if not empresa:
        messages.error(request, "Perfil de empresa não encontrado.")
        return redirect("estagios:list")

    candidaturas = (
        Candidatura.objects.filter(estagio__empresa=empresa)
        .select_related("aluno", "estagio", "estagio__empresa")
        .order_by("-data_candidatura")
    )

    context = {
        "candidaturas": candidaturas,
    }
    return render(request, "candidaturas/empresa_candidaturas.html", context)


@login_required
@role_required("EMPRESA", message="Acesso restrito a empresas.")
def alterar_estado(request, pk, novo_estado):
    empresa = get_empresa_profile(request.user)
    if not empresa:
        messages.error(request, "Perfil de empresa não encontrado.")
        return redirect("estagios:list")

    estados_validos = {"ACEITE", "REJEITADO", "PENDENTE"}
    if novo_estado not in estados_validos:
        messages.error(request, "Estado inválido.")
        return redirect("candidaturas:empresa_list")

    candidatura = get_object_or_404(
        Candidatura,
        pk=pk,
        estagio__empresa=empresa,
    )

    candidatura.status = novo_estado
    candidatura.save(update_fields=["status"])

    messages.success(request, f"Estado atualizado para {novo_estado}.")
    return redirect("candidaturas:empresa_list")


@login_required
@role_required("ALUNO", message="Acesso restrito a alunos.")
def acompanhamento_estagio(request, pk):
    candidatura = get_object_or_404(
        Candidatura.objects.select_related("estagio", "estagio__empresa"),
        pk=pk,
        aluno=request.user,
    )

    relatorio = getattr(candidatura, "relatorio", None)
    avaliacao = getattr(candidatura, "avaliacao", None)
    certificado = getattr(candidatura, "certificado_pdf", None)

    context = {
        "candidatura": candidatura,
        "relatorio": relatorio,
        "avaliacao": avaliacao,
        "certificado": certificado,
    }
    return render(request, "candidaturas/acompanhamento.html", context)