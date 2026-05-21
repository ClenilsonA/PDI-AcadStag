from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from core.decorators import role_required
from processos.models import ProcessoEstagio

from .forms import CertificadoForm


@login_required
@role_required("ADMIN", message="Acesso restrito aos serviços académicos.")
def emitir_certificado(request, processo_id):
    processo = get_object_or_404(
        ProcessoEstagio.objects.select_related(
            "candidatura",
            "candidatura__aluno",
            "candidatura__estagio",
            "candidatura__estagio__empresa",
        ),
        pk=processo_id,
    )

    if not processo.pode_emitir_certificado:
        messages.error(
            request,
            "Só é possível emitir certificado depois do processo estar concluído e da nota final estar publicada.",
        )
        return redirect("processos:detalhe", pk=processo.pk)

    certificado = getattr(processo, "certificado", None)

    if request.method == "POST":
        form = CertificadoForm(request.POST, request.FILES, instance=certificado)

        if form.is_valid():
            certificado_guardado = form.save(commit=False)
            certificado_guardado.processo = processo
            certificado_guardado.emitido_por = request.user
            certificado_guardado.save()

            messages.success(request, "Certificado guardado com sucesso.")
            return redirect("processos:detalhe", pk=processo.pk)
    else:
        form = CertificadoForm(instance=certificado)

    context = {
        "form": form,
        "processo": processo,
        "certificado": certificado,
    }
    return render(request, "certificados/emitir_certificado.html", context)


@login_required
@role_required("ALUNO", message="Acesso restrito a alunos.")
def aluno_certificado(request, processo_id):
    processo = get_object_or_404(
        ProcessoEstagio.objects.select_related(
            "candidatura",
            "candidatura__aluno",
            "candidatura__estagio",
            "candidatura__estagio__empresa",
        ),
        pk=processo_id,
        candidatura__aluno=request.user,
    )

    if not processo.certificado_disponivel_para_aluno:
        messages.error(request, "O certificado ainda não está disponível.")
        return redirect("candidaturas:minhas")

    certificado = processo.certificado

    context = {
        "processo": processo,
        "certificado": certificado,
    }
    return render(request, "certificados/aluno_certificado.html", context)