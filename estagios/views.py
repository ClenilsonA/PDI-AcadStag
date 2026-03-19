from django.shortcuts import render

# Create your views here.

from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import Estagio

def home(request):
    if request.user.is_authenticated:
        return redirect("estagios:list")
    return render(request, "pages/home.html")
def estagio_list(request):
    qs = Estagio.objects.filter(ativo=True).select_related("empresa").order_by("-data_criacao")

    q = request.GET.get("q", "").strip()
    area = request.GET.get("area", "").strip()
    duracao = request.GET.get("duracao", "").strip()
    ordem = request.GET.get("ordem", "recentes").strip()

    if q:
        qs = qs.filter(
            Q(titulo__icontains=q) |
            Q(descricao__icontains=q) |
            Q(area__icontains=q) |
            Q(empresa__nome__icontains=q)
        )

    if area:
        qs = qs.filter(area__iexact=area)

    if duracao.isdigit():
        qs = qs.filter(duracao_meses=int(duracao))

    if ordem == "antigos":
        qs = qs.order_by("data_criacao")
    else:
        qs = qs.order_by("-data_criacao")

    # opções para o dropdown de áreas (baseado nos estágios ativos)
    areas_disponiveis = (
        Estagio.objects.filter(ativo=True)
        .values_list("area", flat=True)
        .distinct()
        .order_by("area")
    )

    context = {
        "estagios": qs,
        "q": q,
        "area_selecionada": area,
        "duracao_selecionada": duracao,
        "ordem": ordem,
        "areas_disponiveis": areas_disponiveis,
    }
    return render(request, "estagios/estagio_list.html", context)

def estagio_detail(request, pk):
    estagio = get_object_or_404(Estagio, pk=pk, ativo=True)
    return render(request, "estagios/estagio_detail.html", {"estagio": estagio})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from empresas.models import Empresa
from .models import Estagio
from .forms import EstagioForm

def _get_empresa_profile(user):
    # garante que só empresas entram
    if not user.is_authenticated or user.role != "EMPRESA":
        return None
    try:
        return user.empresa
    except Empresa.DoesNotExist:
        return None

@login_required
def empresa_estagios(request):
    empresa = _get_empresa_profile(request.user)
    if not empresa:
        messages.error(request, "Acesso restrito a empresas.")
        return redirect("estagios:list")

    estagios = Estagio.objects.filter(empresa=empresa).order_by("-data_criacao")
    return render(request, "estagios/empresa_estagios.html", {"estagios": estagios})

@login_required
def estagio_create(request):
    empresa = _get_empresa_profile(request.user)
    if not empresa:
        messages.error(request, "Acesso restrito a empresas.")
        return redirect("estagios:list")

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

    return render(request, "estagios/estagio_form.html", {"form": form, "modo": "Criar"})

@login_required
def estagio_update(request, pk):
    empresa = _get_empresa_profile(request.user)
    if not empresa:
        messages.error(request, "Acesso restrito a empresas.")
        return redirect("estagios:list")

    estagio = get_object_or_404(Estagio, pk=pk, empresa=empresa)

    if request.method == "POST":
        form = EstagioForm(request.POST, instance=estagio)
        if form.is_valid():
            form.save()
            messages.success(request, "Estágio atualizado com sucesso!")
            return redirect("estagios:empresa_list")
    else:
        form = EstagioForm(instance=estagio)

    return render(request, "estagios/estagio_form.html", {"form": form, "modo": "Editar"})

@login_required
def estagio_deactivate(request, pk):
    empresa = _get_empresa_profile(request.user)
    if not empresa:
        messages.error(request, "Acesso restrito a empresas.")
        return redirect("estagios:list")

    estagio = get_object_or_404(Estagio, pk=pk, empresa=empresa)
    estagio.ativo = False
    estagio.save()
    messages.success(request, "Estágio desativado.")
    return redirect("estagios:empresa_list")