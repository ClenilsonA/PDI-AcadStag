from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User
from empresas.models import Empresa


TAILWIND_INPUT = "w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"


class BaseTailwindForm:
    def add_tailwind(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-checkbox"
            else:
                field.widget.attrs["class"] = TAILWIND_INPUT

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_tailwind()


class AlunoRegisterForm(BaseTailwindForm, UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "ALUNO"
        user.email = self.cleaned_data.get("email", "")
        if commit:
            user.save()
        return user


class EmpresaRegisterForm(BaseTailwindForm, UserCreationForm):
    email = forms.EmailField(required=True)

    # dados da empresa
    nome = forms.CharField(max_length=200)
    area = forms.CharField(max_length=120, required=False)
    contacto = forms.CharField(max_length=120, required=False)
    morada = forms.CharField(max_length=200, required=False)
    nif = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "EMPRESA"
        user.email = self.cleaned_data.get("email", "")

        if commit:
            user.save()
            Empresa.objects.create(
                user=user,
                nome=self.cleaned_data["nome"],
                area=self.cleaned_data.get("area", ""),
                contacto=self.cleaned_data.get("contacto", ""),
                morada=self.cleaned_data.get("morada", ""),
                nif=self.cleaned_data.get("nif", ""),
            )
        return user