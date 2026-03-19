
from django.urls import path
from . import views

app_name = "candidaturas"

urlpatterns = [
    path("minhas/", views.minhas_candidaturas, name="minhas"),
    path("criar/<int:estagio_id>/", views.criar_candidatura, name="criar"),

    # Área da empresa
    path("empresa/", views.empresa_candidaturas, name="empresa_list"),
    path("empresa/<int:pk>/estado/<str:novo_estado>/", views.alterar_estado, name="alterar_estado"),
    
    path("<int:pk>/acompanhamento/", views.acompanhamento_estagio, name="acompanhamento"),
]