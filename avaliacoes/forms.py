from django import forms

from core.forms import BaseTailwindForm

from .models import AvaliacaoEntidade, AvaliacaoOrientador


class AvaliacaoOrientadorForm(BaseTailwindForm, forms.ModelForm):
    class Meta:
        model = AvaliacaoOrientador
        fields = ["nota_teorica", "comentario"]


class AvaliacaoEntidadeForm(BaseTailwindForm, forms.ModelForm):
    class Meta:
        model = AvaliacaoEntidade
        fields = ["nota_pratica", "comentario"]