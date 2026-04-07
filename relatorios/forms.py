from django import forms

from core.forms import BaseTailwindForm
from .models import Relatorio


class RelatorioForm(BaseTailwindForm):
    class Meta:
        model = Relatorio
        fields = ["ficheiro"]
        labels = {
            "ficheiro": "Relatório (PDF)",
        }
        widgets = {
            "ficheiro": forms.ClearableFileInput(),
        }