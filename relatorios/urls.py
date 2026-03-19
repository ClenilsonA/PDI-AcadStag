
from django.urls import path
from . import views

app_name = "relatorios"

urlpatterns = [
    # aluno
    path("aluno/", views.aluno_relatorios, name="aluno_list"),
    path("aluno/upload/<int:candidatura_id>/", views.upload_relatorio, name="upload"),

    # empresa
    path("empresa/", views.empresa_relatorios, name="empresa_list"),
    path("empresa/<int:pk>/estado/<str:novo_estado>/", views.alterar_estado_relatorio, name="alterar_estado"),
]