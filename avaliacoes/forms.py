from django import forms

from core.forms import BaseTailwindForm

from .models import AvaliacaoEntidade, AvaliacaoOrientador


def validar_nota_0_20(nota):
    if nota is None:
        return nota

    if nota < 0:
        raise forms.ValidationError("A nota não pode ser negativa.")

    if nota > 20:
        raise forms.ValidationError("A nota não pode ser superior a 20.")

    return nota


class AvaliacaoOrientadorForm(BaseTailwindForm, forms.ModelForm):
    class Meta:
        model = AvaliacaoOrientador
        fields = ["nota_teorica", "comentario"]
        widgets = {
            "nota_teorica": forms.NumberInput(attrs={"min": 0, "max": 20, "step": "0.01"}),
        }

    def clean_nota_teorica(self):
        nota = self.cleaned_data.get("nota_teorica")
        return validar_nota_0_20(nota)


class AvaliacaoEntidadeForm(BaseTailwindForm, forms.ModelForm):
    class Meta:
        model = AvaliacaoEntidade
        fields = ["nota_pratica", "comentario"]
        widgets = {
            "nota_pratica": forms.NumberInput(attrs={"min": 0, "max": 20, "step": "0.01"}),
        }

    def clean_nota_pratica(self):
        nota = self.cleaned_data.get("nota_pratica")
        return validar_nota_0_20(nota)