from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class Carrera(models.Model):
    MODALIDAD_CHOICES = [
        ("Presencial", "Presencial"),
        ("Vespertino", "Vespertino"),
        ("Online", "Online"),
        ("Híbrida", "Híbrida"),
    ]

    codigo = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Código de carrera",
    )
    nombre = models.CharField(
        max_length=120,
        verbose_name="Nombre de la carrera",
    )
    facultad = models.CharField(
        max_length=100,
        verbose_name="Facultad o escuela",
    )
    modalidad = models.CharField(
        max_length=20,
        choices=MODALIDAD_CHOICES,
        default="Presencial",
        verbose_name="Modalidad",
    )
    duracion_semestres = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Duración (semestres)",
    )
    arancel_anual = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Arancel anual ($)",
    )
    cupos_disponibles = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="Cupos disponibles",
    )
    anio_inicio = models.IntegerField(
        verbose_name="Año de inicio",
    )
    activa = models.BooleanField(
        default=True,
        verbose_name="Carrera activa",
    )
    creado_en = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de registro",
    )

    class Meta:
        ordering = ["codigo"]
        verbose_name = "Carrera"
        verbose_name_plural = "Carreras"

    def clean(self):
        super().clean()
        if self.anio_inicio is not None and (self.anio_inicio < 1950 or self.anio_inicio > 2026):
            raise ValidationError(
                {"anio_inicio": "El año de inicio debe estar entre 1950 y 2026."}
            )
        if self.arancel_anual is not None and self.arancel_anual <= 0:
            raise ValidationError(
                {"arancel_anual": "El arancel anual debe ser mayor que cero."}
            )
        if self.cupos_disponibles is not None and self.cupos_disponibles < 0:
            raise ValidationError(
                {"cupos_disponibles": "Los cupos disponibles no pueden ser negativos."}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"