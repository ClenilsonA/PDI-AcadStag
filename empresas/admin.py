from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Empresa

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ("nome", "user", "area", "contacto")
    search_fields = ("nome", "user__username")