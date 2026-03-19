
from django import forms
from .models import Estagio

class EstagioForm(forms.ModelForm):
    class Meta:
        model = Estagio
        fields = ["titulo", "descricao", "area", "duracao_meses", "ativo"]