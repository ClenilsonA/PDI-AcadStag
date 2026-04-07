from django import forms
from django.contrib.auth import get_user_model

from core.forms import BaseTailwindForm
from empresas.models import Empresa
from .models import Perfil


User = get_user_model()


class UserForm(BaseTailwindForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(),
            "last_name": forms.TextInput(),
            "email": forms.EmailInput(),
        }


class PerfilForm(BaseTailwindForm):
    class Meta:
        model = Perfil
        fields = ["telefone", "curso"]
        widgets = {
            "telefone": forms.TextInput(),
            "curso": forms.TextInput(),
        }


class EmpresaForm(BaseTailwindForm):
    class Meta:
        model = Empresa
        fields = ["nome", "area", "contacto", "morada", "nif"]
        widgets = {
            "nome": forms.TextInput(),
            "area": forms.TextInput(),
            "contacto": forms.TextInput(),
            "morada": forms.TextInput(),
            "nif": forms.TextInput(),
        }