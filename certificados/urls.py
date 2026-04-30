from django.urls import path

from . import views

app_name = "certificados"

urlpatterns = [
    path(
        "processo/<int:processo_id>/emitir/",
        views.emitir_certificado,
        name="emitir",
    ),
    path(
        "processo/<int:processo_id>/",
        views.aluno_certificado,
        name="aluno_detalhe",
    ),
]