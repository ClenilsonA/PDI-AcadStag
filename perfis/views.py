from django.shortcuts import render

# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import UserForm, PerfilForm, EmpresaForm
from .models import Perfil

@login_required
def perfil_view(request):
    user_form = UserForm(instance=request.user)

    perfil, _ = Perfil.objects.get_or_create(user=request.user)

    empresa_form = None
    perfil_form = None

    if request.user.role == "EMPRESA":
        # usa o related_name="empresa"
        empresa = request.user.empresa
        empresa_form = EmpresaForm(instance=empresa)

        if request.method == "POST":
            user_form = UserForm(request.POST, instance=request.user)
            empresa_form = EmpresaForm(request.POST, instance=empresa)

            if user_form.is_valid() and empresa_form.is_valid():
                user_form.save()
                empresa_form.save()
                messages.success(request, "Perfil da empresa atualizado com sucesso!")
                return redirect("perfis:perfil")

    else:
        perfil_form = PerfilForm(instance=perfil)

        if request.method == "POST":
            user_form = UserForm(request.POST, instance=request.user)
            perfil_form = PerfilForm(request.POST, instance=perfil)

            if user_form.is_valid() and perfil_form.is_valid():
                user_form.save()
                perfil_form.save()
                messages.success(request, "Perfil atualizado com sucesso!")
                return redirect("perfis:perfil")

    return render(request, "perfis/perfil.html", {
        "user_form": user_form,
        "perfil_form": perfil_form,
        "empresa_form": empresa_form,
    })