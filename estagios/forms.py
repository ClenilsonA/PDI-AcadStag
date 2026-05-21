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
            "duracao_meses": forms.NumberInput(attrs={"min": 1}),
            "ativo": forms.CheckboxInput(),
        }

    def clean_duracao_meses(self):
        duracao = self.cleaned_data.get("duracao_meses")

        if duracao is None:
            return duracao

        if duracao < 1:
            raise forms.ValidationError("A duração deve ser de pelo menos 1 mês.")

        return duracao