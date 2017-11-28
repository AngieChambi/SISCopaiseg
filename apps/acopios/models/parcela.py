from django.db import models
from ..models.socio import Socio


class Parcela(models.Model):

    codigo = models.CharField(max_length=8)
    ubicacion = models.CharField(max_length=20)
    area_cultivo = models.DecimalField(
        max_digits=4, decimal_places=2, blank=True, null=True)
    area_desarrollo = models.DecimalField(
        max_digits=4, decimal_places=2, blank=True, null=True)
    prod_estimado_tn = models.DecimalField(
        max_digits=4, decimal_places=2, blank=True, null=True)
    prod_estimado_kg = models.DecimalField(
        max_digits=4, decimal_places=2, blank=True, null=True)
    total_parcelas = models.IntegerField(blank=True, null=True)
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Parcela"
        verbose_name_plural = "Parcelas"

    def __str__(self):
        return self.codigo
