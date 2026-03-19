
from django import forms
from django.contrib.auth import get_user_model
from .models import Perfil
from empresas.models import Empresa

User = get_user_model()

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ["telefone", "curso"]

        widgets = {
            "telefone": forms.TextInput(attrs={"class": "form-control"}),
            "curso": forms.TextInput(attrs={"class": "form-control"}),
        }

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ["nome", "area", "contacto", "morada", "nif"]

        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "area": forms.TextInput(attrs={"class": "form-control"}),
            "contacto": forms.TextInput(attrs={"class": "form-control"}),
            "morada": forms.TextInput(attrs={"class": "form-control"}),
            "nif": forms.TextInput(attrs={"class": "form-control"}),
        }