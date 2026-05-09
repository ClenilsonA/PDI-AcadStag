from django.urls import path

from . import views

app_name = "processos"

urlpatterns = [
    path("", views.lista_processos, name="list"),
    path("<int:pk>/", views.detalhe_processo, name="detalhe"),
    path("<int:pk>/editar/", views.editar_processo, name="editar"),
    path("<int:pk>/empresa/editar/", views.editar_processo_empresa, name="editar_empresa"),

    path("orientador/", views.lista_processos_orientador, name="orientador_lista"),
    path("orientador/<int:pk>/", views.detalhe_processo_orientador, name="orientador_detalhe"),
]