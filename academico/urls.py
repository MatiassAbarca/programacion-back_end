from django.urls import path
from . import views

app_name = "academico"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("carreras/", views.carrera_list, name="carrera_list"),
    path("carreras/nueva/", views.carrera_create, name="carrera_create"),
    path("carreras/<int:pk>/editar/", views.carrera_update, name="carrera_update"),
    path("carreras/<int:pk>/eliminar/", views.carrera_delete, name="carrera_delete"),
]