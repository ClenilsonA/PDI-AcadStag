from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Avaliacao

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ("candidatura", "nota", "data_avaliacao")
    list_filter = ("nota",)