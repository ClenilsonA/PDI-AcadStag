from django.urls import path
from . import views

app_name = "certificados"

urlpatterns = [
    path("upload/<int:candidatura_id>/", views.upload_certificado, name="upload"),
]
