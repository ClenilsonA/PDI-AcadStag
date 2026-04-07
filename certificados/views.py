from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from core.decorators import role_required
from candidaturas.models import Candidatura

from .forms import CertificadoUploadForm


@login_required
@role_required("ORIENTADOR", redirect_url="dashboard:home", message="Apenas orientadores podem enviar certificados.")
def upload_certificado(request, candidatura_id):
    candidatura = get_object_or_404(
        Candidatura.objects.select_related("aluno", "aluno__perfil", "estagio"),
        id=candidatura_id,
    )

    perfil_aluno = getattr(candidatura.aluno, "perfil", None)
    if not perfil_aluno or perfil_aluno.orientador != request.user:
        messages.error(request, "Só podes enviar certificados para alunos que te estão atribuídos.")
        return redirect("avaliacoes:orientador_list")

    if candidatura.status != "ACEITE":
        messages.error(request, "Só é possível enviar certificado para candidaturas aceites.")
        return redirect("avaliacoes:orientador_list")

    if not hasattr(candidatura, "avaliacao"):
        messages.error(request, "Só podes enviar certificado depois da avaliação.")
        return redirect("avaliacoes:orientador_list")

    if request.method == "POST":
        form = CertificadoUploadForm(request.POST, request.FILES, instance=candidatura)

        if form.is_valid():
            form.save()
            messages.success(request, "Certificado enviado com sucesso.")
            return redirect("avaliacoes:orientador_list")
    else:
        form = CertificadoUploadForm(instance=candidatura)

    context = {
        "form": form,
        "candidatura": candidatura,
    }
    return render(request, "certificados/upload_certificado.html", context)