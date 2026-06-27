from django import forms

from core.forms import BaseTailwindForm
from users.models import User

from .models import ProcessoEstagio


def validar_nota_0_20(nota):
    if nota is None:
        return nota

    if nota < 0:
        raise forms.ValidationError("A nota não pode ser negativa.")

    if nota > 20:
        raise forms.ValidationError("A nota não pode ser superior a 20.")

    return nota


class ProcessoAdminForm(BaseTailwindForm, forms.ModelForm):
    orientador = forms.ModelChoiceField(
        queryset=User.objects.filter(role="ORIENTADOR").order_by("username"),
        required=False,
        label="Orientador",
    )

    class Meta:
        model = ProcessoEstagio
        fields = [
            "orientador",
            "empresa_confirmada",
            "validado_servicos_academicos",
            "estado",
            "nota_final",
            "nota_publicada",
        ]
        widgets = {
            "nota_final": forms.NumberInput(
                attrs={
                    "min": 0,
                    "max": 20,
                    "step": "0.01",
                }
            ),
        }

    def clean_nota_final(self):
        nota = self.cleaned_data.get("nota_final")
        return validar_nota_0_20(nota)


class ProcessoEmpresaForm(forms.ModelForm):
    class Meta:
        model = ProcessoEstagio
        fields = [
            "supervisor_nome",
            "supervisor_email",
            "supervisor_telefone",
            "supervisor_cargo",
            "local_estagio",
            "data_inicio",
            "data_fim",
        ]
        widgets = {
            "data_inicio": forms.DateInput(attrs={"type": "date"}),
            "data_fim": forms.DateInput(attrs={"type": "date"}),
        }

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

        self.fields["estado"].widget.attrs["readonly"] = True
        self.fields["estado"].disabled = True

        input_classes = (
            "w-full rounded-lg border border-gray-300 px-3 py-2 "
            "focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        )

        for field in self.fields.values():
            existing_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{input_classes} {existing_classes}".strip()