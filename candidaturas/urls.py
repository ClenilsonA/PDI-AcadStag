from django.urls import path

from . import views

app_name = "candidaturas"

urlpatterns = [
    path("nova/<int:estagio_id>/", views.criar_candidatura, name="criar"),
    path("minhas/", views.minhas_candidaturas, name="minhas"),
    path("empresa/", views.empresa_candidaturas, name="empresa_list"),

    path("empresa/<int:pk>/aceitar/", views.aceitar_candidatura, name="aceitar"),
    path("empresa/<int:pk>/rejeitar/", views.rejeitar_candidatura, name="rejeitar"),

    path("<int:pk>/acompanhamento/", views.acompanhamento_estagio, name="acompanhamento"),
]