from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import CarreraCreateForm, CarreraUpdateForm
from .models import Carrera


def inicio(request):
    total_carreras = Carrera.objects.count()
    carreras_activas = Carrera.objects.filter(activa=True).count()
    total_cupos = sum(Carrera.objects.values_list("cupos_disponibles", flat=True))
    contexto = {
        "total_carreras": total_carreras,
        "carreras_activas": carreras_activas,
        "total_cupos": total_cupos,
    }
    return render(request, "academico/inicio.html", contexto)


def carrera_list(request):
    query = request.GET.get("q", "").strip()
    carreras = Carrera.objects.all()
    if query:
        carreras = carreras.filter(
            Q(codigo__icontains=query)
            | Q(nombre__icontains=query)
            | Q(facultad__icontains=query)
            | Q(modalidad__icontains=query)
        )
    return render(request, "academico/carrera_list.html", {"carreras": carreras, "query": query})


def carrera_create(request):
    if request.method == "POST":
        form = CarreraCreateForm(request.POST)
        if form.is_valid():
            carrera = form.save()
            messages.success(request, f"Carrera '{carrera.nombre}' creada correctamente.")
            return redirect("academico:carrera_list")
        messages.error(request, "Revisa los errores en el formulario de creación.")
    else:
        form = CarreraCreateForm()
    return render(request, "academico/carrera_create.html", {"form": form})


def carrera_update(request, pk):
    carrera = get_object_or_404(Carrera, pk=pk)
    if request.method == "POST":
        form = CarreraUpdateForm(request.POST, instance=carrera)
        if form.is_valid():
            carrera_editada = form.save()
            messages.success(request, f"Carrera '{carrera_editada.nombre}' actualizada correctamente.")
            return redirect("academico:carrera_list")
        messages.error(request, "Revisa los errores en el formulario de edición.")
    else:
        form = CarreraUpdateForm(instance=carrera)
    return render(
        request,
        "academico/carrera_update.html",
        {"form": form, "carrera": carrera},
    )


def carrera_delete(request, pk):
    carrera = get_object_or_404(Carrera, pk=pk)
    if request.method == "POST":
        nombre = carrera.nombre
        carrera.delete()
        messages.success(request, f"Carrera '{nombre}' eliminada correctamente.")
        return redirect("academico:carrera_list")
    return render(request, "academico/carrera_delete_confirm.html", {"carrera": carrera})