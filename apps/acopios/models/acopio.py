from django.db import models
from ..models.socio import Socio


class Acopio(models.Model):
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE)
    fech_acopio = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=False)
    total = models.DecimalField(
        'Total', max_digits=20, decimal_places=2, blank=True, null=True)
    n_ticket = models.IntegerField()

    class Meta:
        verbose_name = "Acopio"
        verbose_name_plural = "Acopios"

    def __str__(self):
        return self.socio.persona.first_name
