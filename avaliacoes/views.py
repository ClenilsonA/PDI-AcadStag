from django.shortcuts import render

# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from candidaturas.models import Candidatura
from .models import Avaliacao
from .forms import AvaliacaoForm


@login_required
def aluno_avaliacoes(request):
    if request.user.role != "ALUNO":
        messages.error(request, "Acesso restrito a alunos.")
        return redirect("estagios:list")

    candidaturas = (
        Candidatura.objects
        .filter(aluno=request.user, status="ACEITE")
        .select_related("estagio")
        .order_by("-data_candidatura")
    )
    return render(request, "avaliacoes/aluno_avaliacoes.html", {"candidaturas": candidaturas})


@login_required
def orientador_avaliacoes(request):
    if request.user.role != "ORIENTADOR":
        messages.error(request, "Acesso restrito a orientadores.")
        return redirect("estagios:list")

    candidaturas = (
        Candidatura.objects
        .filter(status="ACEITE")
        .select_related("aluno", "estagio")
        .order_by("-data_candidatura")
    )
    return render(request, "avaliacoes/orientador_avaliacoes.html", {"candidaturas": candidaturas})


@login_required
def criar_editar_avaliacao(request, candidatura_id):
    if request.user.role != "ORIENTADOR":
        messages.error(request, "Acesso restrito a orientadores.")
        return redirect("estagios:list")

    candidatura = get_object_or_404(Candidatura, id=candidatura_id, status="ACEITE")

    avaliacao = Avaliacao.objects.filter(candidatura=candidatura).first()

    if request.method == "POST":
        form = AvaliacaoForm(request.POST, instance=avaliacao)
        if form.is_valid():
            avaliacao_guardada = form.save(commit=False)
            avaliacao_guardada.candidatura = candidatura
            avaliacao_guardada.save()
            messages.success(request, "Avaliação guardada com sucesso!")
            return redirect("avaliacoes:orientador_list")
    else:
        form = AvaliacaoForm(instance=avaliacao)

    return render(request, "avaliacoes/avaliacao_form.html", {"form": form, "candidatura": candidatura})