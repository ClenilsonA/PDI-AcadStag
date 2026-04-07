from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from core.decorators import role_required
from candidaturas.models import Candidatura

from .forms import AvaliacaoForm
from .models import Avaliacao


@login_required
@role_required("ALUNO", message="Acesso restrito a alunos.")
def aluno_avaliacoes(request):
    candidaturas = (
        Candidatura.objects.filter(aluno=request.user, status="ACEITE")
        .select_related("estagio")
        .order_by("-data_candidatura")
    )

    context = {
        "candidaturas": candidaturas,
    }
    return render(request, "avaliacoes/aluno_avaliacoes.html", context)


@login_required
@role_required("ORIENTADOR", message="Acesso restrito a orientadores.")
def orientador_avaliacoes(request):
    candidaturas = (
        Candidatura.objects.filter(
            status="ACEITE",
            aluno__perfil__orientador=request.user,
        )
        .select_related("aluno", "estagio")
        .order_by("-data_candidatura")
    )

    context = {
        "candidaturas": candidaturas,
    }
    return render(request, "avaliacoes/orientador_avaliacoes.html", context)


@login_required
@role_required("ORIENTADOR", message="Acesso restrito a orientadores.")
def criar_editar_avaliacao(request, candidatura_id):
    candidatura = get_object_or_404(
        Candidatura.objects.select_related("aluno", "aluno__perfil", "estagio"),
        id=candidatura_id,
        status="ACEITE",
    )

    perfil_aluno = getattr(candidatura.aluno, "perfil", None)
    if not perfil_aluno or perfil_aluno.orientador != request.user:
        messages.error(request, "Só podes avaliar alunos que te estão atribuídos.")
        return redirect("avaliacoes:orientador_list")

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

    context = {
        "form": form,
        "candidatura": candidatura,
    }
    return render(request, "avaliacoes/avaliacao_form.html", context)