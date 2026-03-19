
from django.urls import path
from . import views

app_name = "avaliacoes"

urlpatterns = [
    # aluno
    path("aluno/", views.aluno_avaliacoes, name="aluno_list"),

    # orientador
    path("orientador/", views.orientador_avaliacoes, name="orientador_list"),
    path("orientador/criar/<int:candidatura_id>/", views.criar_editar_avaliacao, name="criar_editar"),
]