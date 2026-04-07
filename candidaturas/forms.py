from django import forms

from core.forms import BaseTailwindForm
from .models import Candidatura


class CandidaturaForm(BaseTailwindForm):
    cv = forms.FileField(required=True)

    class Meta:
        model = Candidatura
        fields = ["cv"]
        labels = {
            "cv": "Currículo (PDF)",
        }
        widgets = {
            "cv": forms.ClearableFileInput(),
        }