from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from core.decorators import role_required
from empresas.utils import get_empresa_profile

from .forms import EstagioForm
from .models import Estagio


def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard:home")

    return render(request, "pages/home.html")


def estagio_list(request):
    if request.user.is_authenticated and request.user.role != "ALUNO":
        return redirect("dashboard:home")

    estagios = (
        Estagio.objects.filter(ativo=True)
        .select_related("empresa")
        .order_by("-data_criacao")
    )

    termo_pesquisa = request.GET.get("q", "").strip()
    area = request.GET.get("area", "").strip()
    duracao = request.GET.get("duracao", "").strip()
    ordem = request.GET.get("ordem", "recentes").strip()

    if termo_pesquisa:
        estagios = estagios.filter(
            Q(titulo__icontains=termo_pesquisa)
            | Q(descricao__icontains=termo_pesquisa)
            | Q(area__icontains=termo_pesquisa)
            | Q(empresa__nome__icontains=termo_pesquisa)
        )

    if area:
        estagios = estagios.filter(area__iexact=area)

    if duracao.isdigit():
        estagios = estagios.filter(duracao_meses=int(duracao))

    if ordem == "antigos":
        estagios = estagios.order_by("data_criacao")
    else:
        estagios = estagios.order_by("-data_criacao")

    areas_disponiveis = (
        Estagio.objects.filter(ativo=True)
        .values_list("area", flat=True)
        .distinct()
        .order_by("area")
    )

    context = {
        "estagios": estagios,
        "q": termo_pesquisa,
        "area_selecionada": area,
        "duracao_selecionada": duracao,
        "ordem": ordem,
        "areas_disponiveis": areas_disponiveis,
    }

    return render(request, "estagios/estagio_list.html", context)


def estagio_detail(request, pk):
    if request.user.is_authenticated and request.user.role != "ALUNO":
        return redirect("dashboard:home")

    estagio = get_object_or_404(
        Estagio.objects.select_related("empresa"),
        pk=pk,
        ativo=True,
    )

    context = {
        "estagio": estagio,
    }

    return render(request, "estagios/estagio_detail.html", context)


@login_required
@role_required("EMPRESA", message="Acesso restrito a empresas.")
def empresa_estagios(request):
    empresa = get_empresa_profile(request.user)

    if not empresa:
        messages.error(request, "Perfil de empresa não encontrado.")
        return redirect("dashboard:home")

    estagios = Estagio.objects.filter(empresa=empresa).order_by("-data_criacao")

    context = {
        "estagios": estagios,
    }

    return render(request, "estagios/empresa_estagios.html", context)


@login_required
@role_required("EMPRESA", message="Acesso restrito a empresas.")
def estagio_create(request):
    empresa = get_empresa_profile(request.user)

    if not empresa:
        messages.error(request, "Perfil de empresa não encontrado.")
        return redirect("dashboard:home")

    if request.method == "POST":
        form = EstagioForm(request.POST)

        if form.is_valid():
            estagio = form.save(commit=False)
            estagio.empresa = empresa
            estagio.save()

            messages.success(request, "Estágio criado com sucesso!")
            return redirect("estagios:empresa_list")
    else:
        form = EstagioForm()

    context = {
        "form": form,
        "modo": "Criar",
    }

    return render(request, "estagios/estagio_form.html", context)


@login_required
@role_required("EMPRESA", message="Acesso restrito a empresas.")
def estagio_update(request, pk):
    empresa = get_empresa_profile(request.user)

    if not empresa:
        messages.error(request, "Perfil de empresa não encontrado.")
        return redirect("dashboard:home")

    estagio = get_object_or_404(Estagio, pk=pk, empresa=empresa)

    if request.method == "POST":
        form = EstagioForm(request.POST, instance=estagio)

        if form.is_valid():
            form.save()
            messages.success(request, "Estágio atualizado com sucesso!")
            return redirect("estagios:empresa_list")
    else:
        form = EstagioForm(instance=estagio)

    context = {
        "form": form,
        "modo": "Editar",
    }

    return render(request, "estagios/estagio_form.html", context)


@login_required
@role_required("EMPRESA", message="Acesso restrito a empresas.")
def estagio_deactivate(request, pk):
    empresa = get_empresa_profile(request.user)

    if not empresa:
        messages.error(request, "Perfil de empresa não encontrado.")
        return redirect("dashboard:home")

    estagio = get_object_or_404(Estagio, pk=pk, empresa=empresa)
    estagio.ativo = False
    estagio.save(update_fields=["ativo"])

    messages.success(request, "Estágio desativado.")
    return redirect("estagios:empresa_list")    