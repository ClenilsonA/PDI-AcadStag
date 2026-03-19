
from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_confirm, name="logout"),
    path("logout/confirm/", views.logout_view, name="logout_confirm"),
    path("registar/", views.register_choice, name="register"),
    path("registar/aluno/", views.register_aluno, name="register_aluno"),
    path("registar/empresa/", views.register_empresa, name="register_empresa"),
]