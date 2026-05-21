from django import forms

from core.forms import BaseTailwindForm
from core.validators import validate_pdf_file

from .models import Certificado


class CertificadoForm(BaseTailwindForm, forms.ModelForm):
    class Meta:
        model = Certificado
        fields = [
            "ficheiro",
            "observacoes",
            "ativo",
        ]
        labels = {
            "ficheiro": "Certificado (PDF)",
            "observacoes": "Observações",
            "ativo": "Certificado ativo",
        }

    def clean_ficheiro(self):
        ficheiro = self.cleaned_data.get("ficheiro")
        return validate_pdf_file(ficheiro)