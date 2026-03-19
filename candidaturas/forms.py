from django import forms
from .models import Candidatura

class CandidaturaForm(forms.ModelForm):
    cv = forms.FileField(required=True)

    class Meta:
        model = Candidatura
        fields = ["cv"]