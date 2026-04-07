from django import forms

from core.forms import BaseTailwindForm
from .models import Estagio


class EstagioForm(BaseTailwindForm):
    class Meta:
        model = Estagio
        fields = ["titulo", "descricao", "area", "duracao_meses", "ativo"]
        widgets = {
            "titulo": forms.TextInput(),
            "descricao": forms.Textarea(attrs={"rows": 4}),
            "area": forms.TextInput(),
            "duracao_meses": forms.NumberInput(),
            "ativo": forms.CheckboxInput(),
        }