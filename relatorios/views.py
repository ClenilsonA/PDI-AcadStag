from django.shortcuts import render

# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from empresas.models import Empresa
from candidaturas.models import Candidatura
from .models import Relatorio
from .forms import RelatorioForm

def _get_empresa_profile(user):
    if not user.is_authenticated or user.role != "EMPRESA":
        return None
    try:
        return user.empresa
    except Empresa.DoesNotExist:
        return None

@login_required
def aluno_relatorios(request):
    if request.user.role != "ALUNO":
        messages.error(request, "Acesso restrito a alunos.")
        return redirect("estagios:list")

    candidaturas = Candidatura.objects.filter(aluno=request.user, status="ACEITE").select_related("estagio", "estagio__empresa").order_by("-data_candidatura")
    return render(request, "relatorios/aluno_relatorios.html", {"candidaturas": candidaturas})

@login_required
def upload_relatorio(request, candidatura_id):
    if request.user.role != "ALUNO":
        messages.error(request, "Acesso restrito a alunos.")
        return redirect("estagios:list")

    candidatura = get_object_or_404(Candidatura, id=candidatura_id, aluno=request.user, status="ACEITE")

    # se já existe relatório, editamos (substitui ficheiro)
    relatorio, _ = Relatorio.objects.get_or_create(candidatura=candidatura)

    if request.method == "POST":
        form = RelatorioForm(request.POST, request.FILES, instance=relatorio)
        if form.is_valid():
            r = form.save(commit=False)
            r.estado = "PENDENTE"
            r.save()
            messages.success(request, "Relatório submetido com sucesso!")
            return redirect("relatorios:aluno_list")
    else:
        form = RelatorioForm(instance=relatorio)

    return render(request, "relatorios/upload.html", {"form": form, "candidatura": candidatura})

@login_required
def empresa_relatorios(request):
    empresa = _get_empresa_profile(request.user)
    if not empresa:
        messages.error(request, "Acesso restrito a empresas.")
        return redirect("estagios:list")

    relatorios = Relatorio.objects.filter(candidatura__estagio__empresa=empresa).select_related("candidatura", "candidatura__aluno", "candidatura__estagio").order_by("-data_submissao")
    return render(request, "relatorios/empresa_relatorios.html", {"relatorios": relatorios})

@login_required
def alterar_estado_relatorio(request, pk, novo_estado):
    empresa = _get_empresa_profile(request.user)
    if not empresa:
        messages.error(request, "Acesso restrito a empresas.")
        return redirect("estagios:list")

    relatorio = get_object_or_404(Relatorio, pk=pk, candidatura__estagio__empresa=empresa)

    estados_validos = ["APROVADO", "REJEITADO", "PENDENTE"]
    if novo_estado not in estados_validos:
        messages.error(request, "Estado inválido.")
        return redirect("relatorios:empresa_list")

    relatorio.estado = novo_estado
    relatorio.save()
    messages.success(request, f"Relatório atualizado para {novo_estado}.")
    return redirect("relatorios:empresa_list")