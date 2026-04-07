from django import forms

from core.forms import BaseTailwindForm
from candidaturas.models import Candidatura


class CertificadoUploadForm(BaseTailwindForm):
    class Meta:
        model = Candidatura
        fields = ["certificado_pdf"]
        labels = {
            "certificado_pdf": "Certificado (PDF)",
        }
        widgets = {
            "certificado_pdf": forms.ClearableFileInput(),
        }