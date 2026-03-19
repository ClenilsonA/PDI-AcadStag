
from django.urls import path
from . import views

app_name = "estagios"

urlpatterns = [
    path("estagios/", views.estagio_list, name="list"),
    path("estagios/<int:pk>/", views.estagio_detail, name="detail"),

    # empresa
    path("empresa/estagios/", views.empresa_estagios, name="empresa_list"),
    path("empresa/estagios/novo/", views.estagio_create, name="create"),
    path("empresa/estagios/<int:pk>/editar/", views.estagio_update, name="update"),
    path("empresa/estagios/<int:pk>/desativar/", views.estagio_deactivate, name="deactivate"),
]