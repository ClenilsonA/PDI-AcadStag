from django import forms

from core.forms import BaseTailwindForm
from core.validators import validate_pdf_file

from .models import Relatorio


class RelatorioForm(BaseTailwindForm):
    class Meta:
        model = Relatorio
        fields = ["ficheiro"]
        labels = {
            "ficheiro": "Relatório final (PDF)",
        }
        widgets = {
            "ficheiro": forms.ClearableFileInput(),
        }

    def clean_ficheiro(self):
        ficheiro = self.cleaned_data.get("ficheiro")
        return validate_pdf_file(ficheiro)