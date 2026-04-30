from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from core.decorators import role_required
from empresas.utils import get_empresa_profile
from estagios.models import Estagio
from processos.services import criar_ou_obter_processo, atualizar_estado_processo

from .forms import AceitarCandidaturaForm, CandidaturaForm
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

            messages.success(request, "Candidatura submetida com sucesso.")
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
        .select_related("aluno", "estagio", "processo")
        .order_by("-data_candidatura")
    )

    context = {
        "candidaturas": candidaturas,
    }
    return render(request, "candidaturas/empresa_candidaturas.html", context)


@login_required
@role_required("EMPRESA", message="Acesso restrito a empresas.")
def aceitar_candidatura(request, pk):
    empresa = get_empresa_profile(request.user)
    if not empresa:
        messages.error(request, "Perfil de empresa não encontrado.")
        return redirect("estagios:list")

    candidatura = get_object_or_404(
        Candidatura.objects.select_related("estagio", "aluno"),
        pk=pk,
        estagio__empresa=empresa,
    )

    processo_existente = getattr(candidatura, "processo", None)

    if candidatura.status == Candidatura.Status.REJEITADA:
        messages.error(request, "Não podes aceitar uma candidatura já rejeitada.")
        return redirect("candidaturas:empresa_list")

    if candidatura.status == Candidatura.Status.ACEITE and processo_existente:
        messages.info(request, "Esta candidatura já foi aceite.")
        return redirect("candidaturas:empresa_list")

    if request.method == "POST":
        form = AceitarCandidaturaForm(request.POST)

        if form.is_valid():
            candidatura.status = Candidatura.Status.ACEITE
            candidatura.save(update_fields=["status"])

            processo = criar_ou_obter_processo(candidatura)
            processo.supervisor_nome = form.cleaned_data["supervisor_nome"]
            processo.supervisor_email = form.cleaned_data["supervisor_email"]
            processo.supervisor_telefone = form.cleaned_data["supervisor_telefone"]
            processo.supervisor_cargo = form.cleaned_data["supervisor_cargo"]
            processo.local_estagio = form.cleaned_data["local_estagio"]
            processo.data_inicio = form.cleaned_data["data_inicio"]
            processo.data_fim = form.cleaned_data["data_fim"]
            processo.save()
            atualizar_estado_processo(processo)

            messages.success(
                request,
                "Candidatura aceite e dados do estágio definidos com sucesso.",
            )
            return redirect("candidaturas:empresa_list")
    else:
        initial = {}

        if processo_existente:
            initial = {
                "supervisor_nome": processo_existente.supervisor_nome,
                "supervisor_email": processo_existente.supervisor_email,
                "supervisor_telefone": processo_existente.supervisor_telefone,
                "supervisor_cargo": processo_existente.supervisor_cargo,
                "local_estagio": processo_existente.local_estagio,
                "data_inicio": processo_existente.data_inicio,
                "data_fim": processo_existente.data_fim,
            }

        form = AceitarCandidaturaForm(initial=initial)

    context = {
        "candidatura": candidatura,
        "form": form,
    }
    return render(request, "candidaturas/aceitar_candidatura.html", context)


@login_required
@role_required("EMPRESA", message="Acesso restrito a empresas.")
def rejeitar_candidatura(request, pk):
    empresa = get_empresa_profile(request.user)
    if not empresa:
        messages.error(request, "Perfil de empresa não encontrado.")
        return redirect("estagios:list")

    candidatura = get_object_or_404(
        Candidatura,
        pk=pk,
        estagio__empresa=empresa,
    )

    if candidatura.status == Candidatura.Status.ACEITE:
        messages.error(request, "Não podes rejeitar uma candidatura já aceite.")
        return redirect("candidaturas:empresa_list")

    candidatura.status = Candidatura.Status.REJEITADA
    candidatura.save(update_fields=["status"])

    messages.success(request, "Candidatura rejeitada com sucesso.")
    return redirect("candidaturas:empresa_list")


@login_required
@role_required("ALUNO", message="Acesso restrito a alunos.")
def acompanhamento_estagio(request, pk):
    candidatura = get_object_or_404(
        Candidatura.objects.select_related(
            "estagio",
            "estagio__empresa",
            "processo",
            "processo__orientador",
        ),
        pk=pk,
        aluno=request.user,
    )

    processo = getattr(candidatura, "processo", None)
    relatorio = getattr(candidatura, "relatorio", None)
    avaliacao = getattr(candidatura, "avaliacao", None)

    context = {
        "candidatura": candidatura,
        "processo": processo,
        "relatorio": relatorio,
        "avaliacao": avaliacao,
    }
    return render(request, "candidaturas/acompanhamento.html", context)