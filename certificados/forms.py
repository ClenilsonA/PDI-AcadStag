from django import forms
from candidaturas.models import Candidatura

class CertificadoUploadForm(forms.ModelForm):
    class Meta:
        model = Candidatura
        fields = ["certificado_pdf"]