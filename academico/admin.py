from django.contrib import admin
from .models import Carrera


@admin.register(Carrera)
class CarreraAdmin(admin.ModelAdmin):
    list_display = (
        "codigo",
        "nombre",
        "facultad",
        "modalidad",
        "duracion_semestres",
        "arancel_anual",
        "cupos_disponibles",
        "anio_inicio",
        "activa",
    )
    search_fields = ("codigo", "nombre", "facultad")
    list_filter = ("modalidad", "activa")