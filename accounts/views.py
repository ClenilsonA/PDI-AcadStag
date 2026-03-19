#from django.shortcuts import render

# Create your views here.

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AlunoRegisterForm, EmpresaRegisterForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect("estagios:list")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("estagios:list")
        else:
            messages.error(request, "Credenciais inválidas.")

    return render(request, "accounts/login.html")

def logout_view(request):
    logout(request)
    return redirect("estagios:list")
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
    return render(request, "accounts/register_aluno.html", {"form": form})

def register_empresa(request):
    if request.method == "POST":
        form = EmpresaRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Conta de empresa criada com sucesso!")
            return redirect("estagios:empresa_list")
    else:
        form = EmpresaRegisterForm()
    return render(request, "accounts/register_empresa.html", {"form": form})