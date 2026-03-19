
from django import forms
from .models import Relatorio

class RelatorioForm(forms.ModelForm):
    class Meta:
        model = Relatorio
        fields = ["ficheiro"]