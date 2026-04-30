from django.urls import path

from . import views

app_name = "avaliacoes"

urlpatterns = [
    path(
        "empresa/processo/<int:processo_id>/",
        views.avaliar_estagio_empresa,
        name="avaliar_empresa",
    ),
    path(
        "orientador/processo/<int:processo_id>/",
        views.avaliar_estagio_orientador,
        name="avaliar_orientador",
    ),
]