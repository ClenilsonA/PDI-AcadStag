from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages

from candidaturas.models import Candidatura
from .forms import CertificadoUploadForm

@login_required
def upload_certificado(request, candidatura_id):
    if request.user.role != "ORIENTADOR":
        messages.error(request, "Apenas orientadores podem enviar certificados.")
        return redirect("dashboard:home")

    candidatura = get_object_or_404(Candidatura, id=candidatura_id)

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

    return render(request, "certificados/upload_certificado.html", {
        "form": form,
        "candidatura": candidatura,
    })
