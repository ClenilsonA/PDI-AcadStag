from django import forms

from core.forms import BaseTailwindForm
from .models import Candidatura


class CandidaturaForm(BaseTailwindForm, forms.ModelForm):
    class Meta:
        model = Candidatura
        fields = [
            "cv",
            "comprovativo_frequencia",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["cv"].required = True
        self.fields["cv"].label = "Curriculum Vitae (PDF)"

        self.fields["comprovativo_frequencia"].required = True
        self.fields["comprovativo_frequencia"].label = (
            "Comprovativo de frequência universitária (PDF)"
        )


class AceitarCandidaturaForm(forms.Form):
    supervisor_nome = forms.CharField(
        max_length=150,
        label="Nome do supervisor",
    )
    supervisor_email = forms.EmailField(
        required=False,
        label="Email do supervisor",
    )
    supervisor_telefone = forms.CharField(
        max_length=30,
        required=False,
        label="Telefone do supervisor",
    )
    supervisor_cargo = forms.CharField(
        max_length=120,
        required=False,
        label="Cargo do supervisor",
    )

    local_estagio = forms.CharField(
        max_length=200,
        label="Local do estágio",
    )

    data_inicio = forms.DateField(
        label="Data de início",
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    data_fim = forms.DateField(
        label="Data de fim",
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get("data_inicio")
        data_fim = cleaned_data.get("data_fim")

        if data_inicio and data_fim and data_fim < data_inicio:
            self.add_error(
                "data_fim",
                "A data de fim não pode ser anterior à data de início.",
            )

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        input_classes = (
            "w-full rounded-lg border border-gray-300 px-3 py-2 "
            "focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        )

        for field in self.fields.values():
            existing_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{input_classes} {existing_classes}".strip()