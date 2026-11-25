from django import forms
from .models import Carrera


class BaseCarreraForm(forms.ModelForm):
    arancel_anual = forms.CharField(
        label="Arancel anual ($)",
        required=True,
    )

    def clean_codigo(self):
        codigo = self.cleaned_data.get("codigo", "").strip().upper()
        if not codigo:
            raise forms.ValidationError("El código de carrera es obligatorio.")
        return codigo

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre", "").strip()
        if len(nombre) < 3:
            raise forms.ValidationError("Ingresa un nombre de carrera válido (mínimo 3 caracteres).")
        return nombre

    def clean_arancel_anual(self):
        valor = str(self.cleaned_data.get("arancel_anual", "")).strip()
        # Quitar puntos de miles o espacios, y si pusieron ",00" o ".00" al final, quitarlo
        limpio = valor.replace(".", "").replace(" ", "").replace("$", "")
        if "," in limpio:
            limpio = limpio.split(",")[0]

        if not limpio.isdigit():
            raise forms.ValidationError("Ingresa un monto numérico válido (ej: 4.500.000).")

        arancel = int(limpio)
        if arancel <= 0:
            raise forms.ValidationError("El arancel anual debe ser un número mayor que 0.")
        return arancel

    def clean_cupos_disponibles(self):
        cupos = self.cleaned_data.get("cupos_disponibles")
        if cupos is None or cupos < 0:
            raise forms.ValidationError("Los cupos disponibles no pueden ser negativos.")
        return cupos

    def clean_anio_inicio(self):
        anio = self.cleaned_data.get("anio_inicio")
        if anio is None or anio < 1950 or anio > 2026:
            raise forms.ValidationError("El año de inicio debe estar entre 1950 y 2026.")
        return anio

    def _aplicar_estilos_bootstrap(self):
        for _, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = "form-select"
            else:
                field.widget.attrs["class"] = "form-control"


class CarreraCreateForm(BaseCarreraForm):
    class Meta:
        model = Carrera
        fields = [
            "codigo",
            "nombre",
            "facultad",
            "modalidad",
            "duracion_semestres",
            "arancel_anual",
            "cupos_disponibles",
            "anio_inicio",
            "activa",
        ]
        widgets = {
            "codigo": forms.TextInput(attrs={"placeholder": "Ej: INF-01"}),
            "nombre": forms.TextInput(attrs={"placeholder": "Ej: Ingeniería en Informática"}),
            "facultad": forms.TextInput(attrs={"placeholder": "Ej: Facultad de Ingeniería"}),
            "arancel_anual": forms.TextInput(attrs={"placeholder": "Ej: 4.500.000"}),
            "duracion_semestres": forms.NumberInput(attrs={"min": 1}),
            "cupos_disponibles": forms.NumberInput(attrs={"min": 0}),
            "anio_inicio": forms.NumberInput(attrs={"min": 1950, "max": 2026}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._aplicar_estilos_bootstrap()


class CarreraUpdateForm(BaseCarreraForm):
    class Meta:
        model = Carrera
        fields = [
            "codigo",
            "nombre",
            "facultad",
            "modalidad",
            "duracion_semestres",
            "arancel_anual",
            "cupos_disponibles",
            "anio_inicio",
            "activa",
        ]
        widgets = {
            "arancel_anual": forms.TextInput(attrs={"placeholder": "Ej: 4.500.000"}),
            "duracion_semestres": forms.NumberInput(attrs={"min": 1}),
            "cupos_disponibles": forms.NumberInput(attrs={"min": 0}),
            "anio_inicio": forms.NumberInput(attrs={"min": 1950, "max": 2026}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.arancel_anual is not None:
            self.initial["arancel_anual"] = f"{self.instance.arancel_anual:,}".replace(",", ".")
        self._aplicar_estilos_bootstrap()