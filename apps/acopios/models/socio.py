from django.db import models
from apps.params.models import Person


class Socio(models.Model):

    persona = models.OneToOneField(Person, on_delete=models.CASCADE)
    cod_socio = models.CharField(max_length=6)
    direccion = models.CharField(max_length=50, blank=True)
    ciudad = models.CharField(max_length=50, blank=True)
    estado = models.BooleanField(default=True)

    updated_at = models.DateTimeField("Updated at", auto_now=True)
    created_at = models.DateTimeField("Created at", auto_now_add=True)

    class Meta:
        verbose_name = "Socio"
        verbose_name_plural = "Socios"

    def __str__(self):
        return self.persona.first_name
