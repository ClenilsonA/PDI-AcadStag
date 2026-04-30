from django.urls import path

from . import views

app_name = "relatorios"

urlpatterns = [
    path("", views.aluno_relatorios, name="aluno_list"),
    path("upload/<int:candidatura_id>/", views.upload_relatorio, name="upload"),
]