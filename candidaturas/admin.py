from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Candidatura

@admin.register(Candidatura)
class CandidaturaAdmin(admin.ModelAdmin):
    list_display = ("aluno", "estagio", "status", "data_candidatura")
    list_filter = ("status",)
    search_fields = ("aluno__username", "estagio__titulo")