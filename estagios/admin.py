from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Estagio

@admin.register(Estagio)
class EstagioAdmin(admin.ModelAdmin):
    list_display = ("titulo", "empresa", "area", "ativo", "data_criacao")
    list_filter = ("ativo", "area")
    search_fields = ("titulo",)