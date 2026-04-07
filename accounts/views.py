from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import AlunoRegisterForm, EmpresaRegisterForm


def _get_login_redirect_url(user):
    if user.role in {"EMPRESA", "ORIENTADOR"}:
        return "dashboard:home"

    return "estagios:list"


def login_view(request):
    if request.user.is_authenticated:
        return redirect(_get_login_redirect_url(request.user))

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(_get_login_redirect_url(user))

        messages.error(request, "Credenciais inválidas.")

    return render(request, "accounts/login.html")


def logout_confirm(request):
    return render(request, "accounts/logout_confirm.html")


def logout_view(request):
    logout(request)
    return redirect("accounts:login")


def register_choice(request):
    return render(request, "accounts/register_choice.html")


def register_aluno(request):
    if request.method == "POST":
        form = AlunoRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Conta de aluno criada com sucesso!")
            return redirect("estagios:list")
    else:
        form = AlunoRegisterForm()

    context = {
        "form": form,
    }
    return render(request, "accounts/register_aluno.html", context)


def register_empresa(request):
    if request.method == "POST":
        form = EmpresaRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Conta de empresa criada com sucesso!")
            return redirect("dashboard:home")
    else:
        form = EmpresaRegisterForm()

    context = {
        "form": form,
    }
    return render(request, "accounts/register_empresa.html", context)