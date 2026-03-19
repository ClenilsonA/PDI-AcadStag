from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Relatorio

@admin.register(Relatorio)
class RelatorioAdmin(admin.ModelAdmin):
    list_display = ("candidatura", "estado", "data_submissao")
    list_filter = ("estado",)