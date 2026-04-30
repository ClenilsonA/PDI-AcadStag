from django import forms

from core.forms import BaseTailwindForm

from .models import Certificado


class CertificadoForm(BaseTailwindForm, forms.ModelForm):
    class Meta:
        model = Certificado
        fields = [
            "ficheiro",
            "observacoes",
            "ativo",
        ]