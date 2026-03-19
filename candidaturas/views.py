from django.shortcuts import render

# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages

from estagios.models import Estagio
from .models import Candidatura
from .forms import CandidaturaForm

@login_required
def criar_candidatura(request, estagio_id):
    if request.user.role != "ALUNO":
        messages.error(request, "Apenas alunos podem candidatar-se.")
        return redirect("estagios:list")

    estagio = get_object_or_404(Estagio, id=estagio_id, ativo=True)

    # impedir duplicados
    if Candidatura.objects.filter(aluno=request.user, estagio=estagio).exists():
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

    return render(
        request,
        "candidaturas/candidatura_form.html",
        {
            "form": form,
            "estagio": estagio
        }
    )
    return redirect("candidaturas:minhas")

@login_required
def minhas_candidaturas(request):
    if request.user.role != "ALUNO":
        messages.error(request, "Apenas alunos têm candidaturas.")
        return redirect("estagios:list")

    candidaturas = Candidatura.objects.filter(aluno=request.user).order_by("-data_candidatura")
    return render(request, "candidaturas/minhas_candidaturas.html", {"candidaturas": candidaturas})

#
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from empresas.models import Empresa
from .models import Candidatura

def _get_empresa_profile(user):
    if not user.is_authenticated or user.role != "EMPRESA":
        return None
    try:
        return user.empresa
    except Empresa.DoesNotExist:
        return None

@login_required
def empresa_candidaturas(request):
    empresa = _get_empresa_profile(request.user)
    if not empresa:
        messages.error(request, "Acesso restrito a empresas.")
        return redirect("estagios:list")

    candidaturas = Candidatura.objects.filter(estagio__empresa=empresa).select_related("aluno", "estagio").order_by("-data_candidatura")
    return render(request, "candidaturas/empresa_candidaturas.html", {"candidaturas": candidaturas})

@login_required
def alterar_estado(request, pk, novo_estado):
    empresa = _get_empresa_profile(request.user)
    if not empresa:
        messages.error(request, "Acesso restrito a empresas.")
        return redirect("estagios:list")

    candidatura = get_object_or_404(Candidatura, pk=pk, estagio__empresa=empresa)

    estados_validos = ["ACEITE", "REJEITADO", "PENDENTE"]
    if novo_estado not in estados_validos:
        messages.error(request, "Estado inválido.")
        return redirect("candidaturas:empresa_list")

    candidatura.status = novo_estado
    candidatura.save()
    messages.success(request, f"Estado atualizado para {novo_estado}.")
    return redirect("candidaturas:empresa_list")

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Candidatura

@login_required
def acompanhamento_estagio(request, pk):
    if request.user.role != "ALUNO":
        messages.error(request, "Acesso restrito a alunos.")
        return redirect("estagios:list")

    candidatura = get_object_or_404(Candidatura, pk=pk, aluno=request.user)

    # estes campos existem graças aos related_name:
    relatorio = getattr(candidatura, "relatorio", None)
    avaliacao = getattr(candidatura, "avaliacao", None)

    return render(
        request,
        "candidaturas/acompanhamento.html",
        {
            "candidatura": candidatura,
            "relatorio": relatorio,
            "avaliacao": avaliacao,
        },
    )